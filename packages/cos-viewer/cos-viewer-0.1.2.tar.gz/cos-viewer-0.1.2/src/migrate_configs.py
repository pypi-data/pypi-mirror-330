from config_manager import ConfigManager
from pathlib import Path
import configparser
import json
import datetime

def migrate_configs():
    # 迁移旧版INI配置
    old_config_path = Path.home() / ".cos-viewer" / "config.ini"
    if old_config_path.exists():
        migrate_ini_config(old_config_path)
    
    # 迁移新版配置结构
    cm = ConfigManager()
    configs = cm.list_configs()
    
    for config_name in configs:
        config = cm.get_config(config_name)
        
        # 如果缺少新字段则补充
        if 'history' not in config:
            cm.config_data[config_name]['history'] = []
        if 'created_at' not in config:
            cm.config_data[config_name]['created_at'] = datetime.datetime.now().isoformat()
        if 'updated_at' not in config:
            cm.config_data[config_name]['updated_at'] = datetime.datetime.now().isoformat()
            
    cm._save()
    print(f"成功迁移 {len(configs)} 个配置")

def migrate_ini_config(config_path):
    """迁移旧版INI格式配置到新版JSON格式"""
    cm = ConfigManager()
    parser = configparser.ConfigParser()
    parser.read(config_path)
    
    for section in parser.sections():
        config = dict(parser[section])
        
        # 转换键名到小写
        key_mapping = {
            'COS_SECRET_ID': 'cos_secret_id',
            'COS_SECRET_KEY': 'cos_secret_key',
            'COS_REGION': 'cos_region',
            'COS_BUCKET': 'cos_bucket',
            'PREFIX': 'prefix'
        }
        
        new_config = {}
        for old_key, new_key in key_mapping.items():
            if old_key in config:
                new_config[new_key] = config[old_key]
        
        # 创建新配置并保留原始创建时间
        try:
            cm.create_config(
                section,
                new_config['cos_secret_id'],
                new_config['cos_secret_key'],
                new_config['cos_region'],
                new_config['cos_bucket'],
                new_config['prefix']
            )
            # 手动设置创建时间为旧配置最后修改时间
            create_time = datetime.datetime.fromtimestamp(
                config_path.stat().st_mtime
            ).isoformat()
            cm.config_data[section]['created_at'] = create_time
            cm.config_data[section]['updated_at'] = create_time
        except ValueError:
            continue
            
    cm._save()
    # 删除旧配置文件
    config_path.unlink()

if __name__ == "__main__":
    migrate_configs()
