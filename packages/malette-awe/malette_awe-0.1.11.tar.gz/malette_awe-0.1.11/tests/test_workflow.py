import pytest
from unittest.mock import patch, MagicMock
from awe.util.workflow import contains_chinese, convert_to_old_data, convert_to_old_result, translate, get_workflow_data
from awe.types.common import Payload, ResponseMessage

def test_contains_chinese():
    """测试中文检测"""
    assert contains_chinese("你好") == True
    assert contains_chinese("Hello") == False
    assert contains_chinese("Hello你好") == True
    assert contains_chinese("") == False

@patch('awe.util.workflow.tongyi_translate')
def test_translate(mock_translate):
    """测试翻译功能"""
    mock_translate.return_value = "beautiful girl"
    
    # 测试中文翻译
    result = translate("漂亮的女孩")
    assert result == "beautiful girl"
    mock_translate.assert_called_once_with("漂亮的女孩")
    
    # 测试英文不翻译
    result = translate("beautiful girl")
    assert result == "beautiful girl"

def test_get_workflow_data():
    """测试获取工作流数据"""
    # 测试直接包含workflow的情况
    payload = Payload(
        taskId="123",
        workflow={"test": "data"}
    )
    result = get_workflow_data(payload)
    assert result == {"test": "data"}
    
    # 测试空workflow的情况
    payload = Payload(taskId="123")
    result = get_workflow_data(payload)
    assert result is None 
    
def test_convert_to_old_result():
    """测试转换为老版本的结果"""
    message = ResponseMessage({
        "response": {
            "data": {
            "images": {"output": [{"filename": "", "subfolder": "", "type": "output", "url": "http://nhci-aigc.oss-cn-zhangjiakou.aliyuncs.com/2024%2F12%2F20%2FXAc8xqvnUA.webp?OSSAccessKeyId=LTAI5tCv9DpB7gYic1oGsAyv&Expires=1734695350&Signature=uvosd4%2BTIkmzE26G9WaFgO9Hu2I%3D", "path": "2024/12/20/XAc8xqvnUA.webp"}]},
            "lt": {"output": ["243,13"]},
            "rb": {"output": ["1230,1470"]},
            "size": {"output": ["1500,1500"]}
        }
    }})
    result = convert_to_old_result(message)
    assert result == [
        {"filename": "", "subfolder": "", "type": "output", "url": "http://nhci-aigc.oss-cn-zhangjiakou.aliyuncs.com/2024%2F12%2F20%2FXAc8xqvnUA.webp?OSSAccessKeyId=LTAI5tCv9DpB7gYic1oGsAyv&Expires=1734695350&Signature=uvosd4%2BTIkmzE26G9WaFgO9Hu2I%3D", "path": "2024/12/20/XAc8xqvnUA.webp"}
    ]
    
def test_convert_to_old_data():
    """测试转换为老版本的数据"""
    message = ResponseMessage({
        "response": {
            "data": {
                "images": {"output": []},
                "lt": {"output": ["243,13"]},
                "rb": {"output": ["1230,1470"]},
                "size": {"output": ["1500,1500"]}
            }
        }
    })
    result = convert_to_old_data(message)
    assert result == {"images": [], "lt": ["243,13"], "rb": ["1230,1470"], "size": ["1500,1500"]}
    
