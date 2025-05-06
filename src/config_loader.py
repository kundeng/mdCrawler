"""Configuration loader and processor for documentation crawlers."""

import re
import yaml
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass

@dataclass
class CleaningRule:
    """A rule for cleaning documentation text."""
    pattern: str
    replace: Optional[str] = None
    replace_fn: Optional[str] = None
    flags: List[str] = None

    def get_flags(self) -> int:
        """Convert string flags to re module flags."""
        if not self.flags:
            return 0
        
        flag_map = {
            'IGNORECASE': re.IGNORECASE,
            'MULTILINE': re.MULTILINE,
            'DOTALL': re.DOTALL,
            'ASCII': re.ASCII,
            'VERBOSE': re.VERBOSE
        }
        
        result = 0
        for flag in self.flags:
            if flag in flag_map:
                result |= flag_map[flag]
        return result

    def get_replacement(self, match) -> str:
        """Get the replacement string or execute the replacement function."""
        if self.replace is not None:
            # Handle raw string replacements
            if isinstance(self.replace, str) and self.replace.startswith('r'):
                # Strip the 'r' prefix and use the string content directly
                return match.expand(self.replace[2:-1] if self.replace[1] == "'" else self.replace[2:-1])
            return match.expand(self.replace)
        
        if self.replace_fn:
            # Create a local context with re module available
            context = {'re': re, 'match': match}
            
            # Extract the function definition
            fn_def = self.replace_fn.strip()
            
            if fn_def.startswith('lambda'):
                # Handle lambda functions
                fn = eval(fn_def, context)
            else:
                # Handle regular functions
                exec(fn_def, context)
                fn_name = fn_def.split()[1].split('(')[0]
                fn = context[fn_name]
            
            return fn(match)
        
        return match.group(0)

@dataclass
class SiteConfig:
    """Configuration for a documentation site."""
    base_url: str
    url_patterns: List[str]
    crawler: Dict[str, Any]
    markdown: Dict[str, Any]
    cleaning_rules: List[CleaningRule]
    post_process: List[Dict[str, bool]]

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'SiteConfig':
        """Load configuration from a YAML file."""
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Convert cleaning rules to CleaningRule objects
        cleaning_rules = []
        for rule in config.get('cleaning_rules', []):
            cleaning_rules.append(CleaningRule(
                pattern=rule['pattern'],
                replace=rule.get('replace'),
                replace_fn=rule.get('replace_fn'),
                flags=rule.get('flags', [])
            ))
        
        return cls(
            base_url=config['base_url'],
            url_patterns=config['url_patterns'],
            crawler=config['crawler'],
            markdown=config['markdown'],
            cleaning_rules=cleaning_rules,
            post_process=config.get('post_process', [])
        )

    def clean_text(self, text: str) -> str:
        """Apply all cleaning rules to the text."""
        for rule in self.cleaning_rules:
            text = re.sub(
                rule.pattern,
                lambda m: rule.get_replacement(m),
                text,
                flags=rule.get_flags()
            )
        
        # Apply post-processing
        for process in self.post_process:
            for action, enabled in process.items():
                if enabled:
                    if action == 'strip_whitespace':
                        text = text.strip()
                    elif action == 'ensure_single_title':
                        # Ensure only one top-level heading
                        first_heading = True
                        lines = []
                        for line in text.split('\n'):
                            if line.startswith('# '):
                                if first_heading:
                                    lines.append(line)
                                    first_heading = False
                                else:
                                    lines.append('#' + line)  # Demote to h2
                            else:
                                lines.append(line)
                        text = '\n'.join(lines)
                    elif action == 'normalize_headings':
                        # Ensure proper heading hierarchy
                        lines = text.split('\n')
                        min_level = 6
                        # Find minimum heading level
                        for line in lines:
                            if line.startswith('#'):
                                level = len(line) - len(line.lstrip('#'))
                                if level < min_level:
                                    min_level = level
                        # Normalize levels
                        if min_level > 1:
                            text = '\n'.join(
                                line[min_level-1:] if line.startswith('#' * min_level) else line
                                for line in lines
                            )
        
        return text

def load_site_config(site_name: str) -> SiteConfig:
    """Load configuration for a specific documentation site."""
    config_path = f'config/sites/{site_name}.yaml'
    return SiteConfig.from_yaml(config_path)
