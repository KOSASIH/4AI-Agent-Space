"""
🏪 Universal Agent Plugin Registry & Marketplace
Dynamic loading, versioning, monetization ready
"""

import importlib
import pkgutil
from typing import Dict, List, Type, Any, Optional
from dataclasses import dataclass
import yaml
from pathlib import Path

@dataclass
class AgentPlugin:
    name: str
    version: str
    description: str
    capabilities: List[str]  # ["research", "coding", "analysis"]
    agent_class: Type[QuantumAgent]
    price_per_use: Optional[float] = None  # For marketplace
    author: str = "community"
    
    def to_dict(self):
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "capabilities": self.capabilities,
            "price_per_use": self.price_per_use
        }

class AgentRegistry:
    """Central registry for all agent plugins"""
    
    def __init__(self, plugins_dir: str = "src/marketplace/plugins"):
        self.plugins_dir = Path(plugins_dir)
        self.registered_plugins: Dict[str, AgentPlugin] = {}
        self._load_plugins()
    
    def _load_plugins(self):
        """Dynamically discover and load plugins"""
        for importer, modname, ispkg in pkgutil.iter_modules([self.plugins_dir]):
            if ispkg:
                try:
                    module = importlib.import_module(f"marketplace.plugins.{modname}")
                    plugin_info = getattr(module, 'PLUGIN_INFO', None)
                    
                    if plugin_info:
                        plugin_class = getattr(module, plugin_info['agent_class'])
                        plugin = AgentPlugin(
                            name=plugin_info['name'],
                            version=plugin_info['version'],
                            description=plugin_info['description'],
                            capabilities=plugin_info['capabilities'],
                            agent_class=plugin_class,
                            price_per_use=plugin_info.get('price_per_use')
                        )
                        self.registered_plugins[plugin.name] = plugin
                except Exception as e:
                    print(f"Failed to load plugin {modname}: {e}")
    
    def discover_capable_agents(self, task_type: str) -> List[AgentPlugin]:
        """Find agents capable of specific task types"""
        return [
            plugin for plugin in self.registered_plugins.values()
            if task_type.lower() in [cap.lower() for cap in plugin.capabilities]
        ]
    
    def instantiate_agent(self, plugin_name: str, **kwargs) -> QuantumAgent:
        """Instantiate agent from registry"""
        plugin = self.registered_plugins.get(plugin_name)
        if not plugin:
            raise ValueError(f"Plugin {plugin_name} not found")
        return plugin.agent_class(**kwargs)
