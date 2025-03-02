"""
Configuration management for llm-clients
"""
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml
from rich.console import Console

console = Console(stderr=True)

# Configuration paths
CONFIG_PATHS = [
    Path("/etc/llm-clients/config.yaml"),  # System-wide config
    Path.home() / ".config" / "llm-clients" / "config.yaml",  # User config
    Path.cwd() / "llm-clients.yaml",  # Project-specific config
]

# Default configuration
DEFAULT_CONFIG = {
    # Simple provider-to-key mapping
    "providers": {
        "openai": None,      # OpenAI API key
        "anthropic": None,   # Anthropic API key
        "openrouter": None,  # OpenRouter API key
        "sambanova": None,   # SambaNova API key
        "siliconflow": None, # SiliconFlow API key
        "gemini": None,      # Google Gemini API key
        "moonshot": None,    # Moonshot AI API key
        "deepseek": None,    # Deepseek API key
        "minimax": None,     # MiniMax API key
        "tencent": {         # Tencent Hunyuan API credentials
            "secret_id": None,
            "secret_key": None,
        },
    },
    
    # Model configurations
    "models": {
        # Model aliases for easier access
        "aliases": {
            # Anthropic models
            "sonnet": "anthropic:claude-3-7-sonnet-latest",
            "default": "sambanova:Meta-Llama-3.3-70B-Instruct",
        },
        
        # Default parameters for all models
        "defaults": {
            "temperature": 0.3,
            "max_tokens": None,  # Use model-specific defaults
            "top_p": 1.0,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        }
    }
}

class Config:
    def __init__(self):
        self._config: Dict[str, Any] = {}
        self._load_config()

    def resolve_model(self, model: str) -> Tuple[str, str, Optional[Dict[str, Any]]]:
        """Resolve a model name to provider, model name and config
        
        Args:
            model: Model name or alias (e.g. "gpt4", "anthropic:claude-3")
            
        Returns:
            Tuple of (provider_name, model_name, model_config)
            
        Raises:
            ValueError: If model cannot be resolved
        """
        # Load model aliases
        aliases = self.get("models.aliases", {})
        
        # Check if it's an alias
        if model in aliases:
            alias_target = aliases[model]
            if ":" not in alias_target:
                raise ValueError(f"Invalid alias target: {alias_target}")
            model = alias_target
        
        # Split provider and model
        if ":" not in model:
            raise ValueError(f"Invalid model spec: {model}")
            
        provider, model_name = model.split(":", 1)
        
        # Verify provider exists
        if not self.get(f"providers.{provider}"):
            raise ValueError(f"Provider not configured: {provider}")
            
        # Get model config
        model_config = self.get("models.defaults", {}).copy()
        specific_config = self.get(f"models.{model_name}", {})
        model_config.update(specific_config)
            
        return provider, model_name, model_config

    def _load_config(self) -> None:
        """Load configuration from all available sources"""
        # Start with default config
        self._config = DEFAULT_CONFIG.copy()

        # Load from config files in order
        for config_path in CONFIG_PATHS:
            if config_path.exists():
                try:
                    with open(config_path, "r") as f:
                        file_config = yaml.safe_load(f) or {}
                    self._merge_config(file_config)
                except Exception as e:
                    console.print(f"[yellow]Warning: Error loading config from {config_path}: {e}[/yellow]")

        # Load from environment variables
        self._load_env_vars()

    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """Recursively merge new configuration into existing config"""
        # Replace the entire config if it's a top-level update
        if set(new_config.keys()).issubset({"providers", "models"}):
            self._config.update(new_config)
        else:
            # Otherwise merge recursively
            for key, value in new_config.items():
                if isinstance(value, dict) and key in self._config and isinstance(self._config[key], dict):
                    self._merge_dict(self._config[key], value)
                else:
                    self._config[key] = value

    def _merge_dict(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Helper method to recursively merge two dictionaries"""
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._merge_dict(target[key], value)
            else:
                target[key] = value

    def _load_env_vars(self) -> None:
        """Load configuration from environment variables"""
        prefix = "LLM_CLI_"
        for key, value in os.environ.items():
            if key.startswith(prefix):
                config_key = key[len(prefix):].lower().replace("_", ".")
                self.set(config_key, value, save=False)

    def get_model_config(self, model_spec: str) -> Dict[str, Any]:
        """Get complete configuration for a specific model"""
        provider, model, model_config = self.resolve_model(model_spec)
        
        # Start with default config
        config = self._config["models"]["defaults"].copy()
        
        # Add model-specific config
        config.update(model_config)
        
        # Add API key
        config["api_key"] = self.get(f"providers.{provider}")
        
        return config

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value
        
        Args:
            key: Dot-separated configuration key (e.g., "providers.openai")
            default: Default value if key not found
            
        Returns:
            The configuration value, or default if not found
        """
        parts = key.split(".")
        current = self._config
        
        # Navigate to the target key
        for part in parts:
            if not isinstance(current, dict) or part not in current:
                return default
            current = current[part]
            
        return current

    def set(self, key: str, value: Any, save: bool = True) -> None:
        """Set a configuration value
        
        Args:
            key: Dot-separated configuration key (e.g., "providers.openai")
            value: Value to set
            save: Whether to save the configuration to disk
        """
        # Start with a fresh config
        self._load_config()
        
        parts = key.split(".")
        current = self._config
        
        # Navigate to parent of target key
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                current[part] = {}
            current = current[part]
            
        # Set the value
        current[parts[-1]] = value
        
        # Save if requested
        if save:
            # Save only the top-level sections to prevent duplication
            config_to_save = {
                "providers": self._config["providers"],
                "models": self._config["models"]
            }
            config_path = Path.home() / ".config" / "llm-clients" / "config.yaml"
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                with open(config_path, "w") as f:
                    yaml.safe_dump(config_to_save, f, sort_keys=False)
            except Exception as e:
                console.print(f"[yellow]Warning: Error saving config to {config_path}: {e}[/yellow]")

    def add_model_alias(self, alias: str, target: str) -> None:
        """Add a new model alias"""
        # Verify the target is valid
        self.resolve_model(target)  # This will raise ValueError if invalid
        
        # Add the alias
        self.set(f"models.aliases.{alias}", target)

    def delete(self, key: str, save: bool = True) -> None:
        """Delete a configuration value"""
        parts = key.split(".")
        current = self._config
        
        # Navigate to parent of target key
        for part in parts[:-1]:
            if not isinstance(current, dict) or part not in current:
                return
            current = current[part]
            
        # Delete the key if it exists
        if isinstance(current, dict) and parts[-1] in current:
            del current[parts[-1]]
            if save:
                self._save_user_config()

    def _save_user_config(self) -> None:
        """Save user configuration to disk"""
        config_path = Path.home() / ".config" / "llm-clients" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_path, "w") as f:
                yaml.safe_dump(self._config, f, sort_keys=False)
        except Exception as e:
            console.print(f"[yellow]Warning: Error saving config to {config_path}: {e}[/yellow]")

# Global configuration instance
config = Config()