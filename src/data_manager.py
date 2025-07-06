import json
import os
from typing import List, Dict, Any
import shutil

class DataManager:
    """负责处理数据的加载、保存和管理"""
    
    def __init__(self, data_file='invoices.json', cache_dir='cache'):
        """
        初始化数据管理器
        :param data_file: 数据文件的路径
        :param cache_dir: 缓存目录的路径
        """
        self.data_file = data_file
        self.cache_dir = cache_dir
        self.data = self._load_data()
        self._ensure_cache_dir()

    def _ensure_cache_dir(self):
        """确保缓存目录存在"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _load_data(self) -> Dict[str, Any]:
        """从 JSON 文件加载数据，如果文件不存在或损坏，则返回默认结构"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._get_default_data()
        return self._get_default_data()

    def _get_default_data(self) -> Dict[str, Any]:
        """返回默认的数据结构，包含一个示例用户"""
        return {
            "users": ["默认用户"],
            "invoices": {
                "默认用户": [
                    {
                        "id": "INV-2023-001",
                        "invoice_number": "INV-2023-001",
                        "supplier": "示例供应商A",
                        "issue_date": "2023-10-26",
                        "amount": 1500.75,
                        "status": "已支付",
                        "due_date": "2023-11-25",
                        "notes": "这是默认的一条发票记录。"
                    }
                ]
            }
        }

    def _save_data(self):
        """将当前数据保存到 JSON 文件"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Error saving data: {e}")

    def get_users(self) -> List[str]:
        """获取所有用户的列表"""
        return self.data.get("users", [])

    def add_user(self, user_name: str) -> bool:
        """添加一个新用户"""
        if user_name and user_name not in self.data["users"]:
            self.data["users"].append(user_name)
            self.data["invoices"][user_name] = []
            self._save_data()
            return True
        return False

    def delete_user(self, user_name: str) -> bool:
        """删除一个用户及其所有发票"""
        if user_name in self.data["users"]:
            # 不允许删除最后一个用户
            if len(self.data["users"]) == 1:
                return False
            self.data["users"].remove(user_name)
            if user_name in self.data["invoices"]:
                del self.data["invoices"][user_name]
            self._save_data()
            return True
        return False
        
    def rename_user(self, old_name: str, new_name: str) -> bool:
        """重命名用户"""
        if old_name in self.data["users"] and new_name and new_name not in self.data["users"]:
            # 更新用户列表
            user_index = self.data["users"].index(old_name)
            self.data["users"][user_index] = new_name
            # 更新发票数据
            if old_name in self.data["invoices"]:
                self.data["invoices"][new_name] = self.data["invoices"].pop(old_name)
            self._save_data()
            return True
        return False

    def get_invoices(self, user_name: str) -> List[Dict[str, Any]]:
        """获取指定用户的所有发票"""
        return self.data.get("invoices", {}).get(user_name, [])

    def add_invoice(self, user_name: str, invoice_data: Dict[str, Any]):
        """为指定用户添加一张新发票"""
        if user_name in self.data.get("users", []):
            self.data.get("invoices", {}).get(user_name, []).append(invoice_data)
            self._save_data()

    def update_invoice(self, user_name: str, invoice_id: str, new_invoice_data: Dict[str, Any]):
        """更新指定用户的特定发票"""
        user_invoices = self.data.get("invoices", {}).get(user_name)
        if user_invoices is not None:
            for i, invoice in enumerate(user_invoices):
                if invoice.get("id") == invoice_id:
                    user_invoices[i] = new_invoice_data
                    self._save_data()
                    return True
        return False

    def delete_invoice(self, user_name: str, invoice_id: str):
        """删除指定用户的特定发票，并从缓存中删除源文件"""
        user_invoices = self.data.get("invoices", {}).get(user_name)
        if user_invoices is not None:
            invoice_to_delete = -1
            invoice_data = None
            for i, invoice in enumerate(user_invoices):
                if invoice.get("id") == invoice_id:
                    invoice_to_delete = i
                    invoice_data = invoice
                    break
            
            if invoice_to_delete != -1:
                # 删除源文件
                if invoice_data and 'source_file' in invoice_data:
                    source_file_path = invoice_data['source_file']
                    if os.path.exists(source_file_path):
                        try:
                            os.remove(source_file_path)
                        except OSError as e:
                            print(f"Error deleting source file {source_file_path}: {e}")

                del user_invoices[invoice_to_delete]
                self._save_data()
                return True
        return False

    def get_invoice_by_id(self, user, invoice_id):
        """通过ID获取单个发票数据"""
        invoices = self.get_invoices(user)
        return next((inv for inv in invoices if inv.get("id") == invoice_id), None)

    def save_source_file(self, source_path: str, invoice_id: str) -> str:
        """
        将源文件保存到缓存目录
        :param source_path: 源文件的原始路径
        :param invoice_id: 发票ID
        :return: 缓存的文件路径
        """
        if not os.path.exists(source_path):
            return ""

        _, extension = os.path.splitext(source_path)
        destination_filename = f"{invoice_id}{extension}"
        destination_path = os.path.join(self.cache_dir, destination_filename)
        
        try:
            shutil.copy(source_path, destination_path)
            return destination_path
        except IOError as e:
            print(f"Error saving source file: {e}")
            return ""

# 创建一个单例 DataManager 实例，供整个应用程序使用
data_manager = DataManager() 