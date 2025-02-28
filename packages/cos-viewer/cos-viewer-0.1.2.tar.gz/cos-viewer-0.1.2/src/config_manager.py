import os
import json
import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".cos-viewer"
CONFIG_FILE = CONFIG_DIR / "config.json"

class ConfigManager:
    def __init__(self):
        CONFIG_DIR.mkdir(exist_ok=True)
        self.config_data = {}
        
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config_data = json.load(f)
            except json.JSONDecodeError:
                self.config_data = {}

    def create_config(self, name, secret_id, secret_key, region, bucket, prefix):
        if name in self.config_data:
            raise ValueError("配置名称已存在")
            
        self.config_data[name] = {
            'current': {
                'cos_secret_id': secret_id,
                'cos_secret_key': secret_key,
                'cos_region': region,
                'cos_bucket': bucket,
                'prefix': prefix
            },
            'history': [],
            'created_at': datetime.datetime.now().isoformat(),
            'updated_at': datetime.datetime.now().isoformat()
        }
        self._save()

    def list_configs(self):
        return list(self.config_data.keys())

    def get_config(self, name, version=None):
        if name not in self.config_data:
            return None
            
        if version is None:
            return self.config_data[name]['current']
            
        # 查找历史版本
        for entry in reversed(self.config_data[name]['history']):
            if entry['version'] == version:
                return entry['config']
        return None

    def delete_config(self, name):
        if name not in self.config_data:
            raise ValueError("配置不存在")
        del self.config_data[name]
        self._save()

    def update_config(self, name, **kwargs):
        if name not in self.config_data:
            raise ValueError("配置不存在")
            
        current_config = self.config_data[name]['current']
        new_config = current_config.copy()
        
        # 记录变更的字段
        changes = {}
        for key, value in kwargs.items():
            if key in ['cos_secret_id', 'cos_secret_key', 'cos_region', 'cos_bucket', 'prefix']:
                if new_config.get(key) != value:
                    changes[key] = {'old': new_config.get(key), 'new': value}
                    new_config[key] = value
        
        if changes:
            # 保存历史记录
            self.config_data[name]['history'].append({
                'version': datetime.datetime.now().isoformat(),
                'config': current_config.copy(),
                'changes': changes,
                'timestamp': datetime.datetime.now().isoformat()
            })
            self.config_data[name]['current'] = new_config
            self.config_data[name]['updated_at'] = datetime.datetime.now().isoformat()
            self._save()

    def _save(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config_data, f, indent=2, ensure_ascii=False)
