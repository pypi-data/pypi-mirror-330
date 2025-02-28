# Pyrilog

一个用于生成 Verilog 代码的 Python 工具。使用 Python 的上下文管理器特性，以简洁的方式生成 Verilog 代码。

## 安装

使用 uv 安装：

```bash
uv pip install pyrilog
```

## 使用示例

```python
from pyrilog import ModuleBlock, IfBlock, ElseBlock, add_parameter, add_assign

with ModuleBlock("Test"):
    add_parameter("PARAM_A", "32")
    with IfBlock("rstn"):
        add_assign("out_data", [], "in_data", [])
    with ElseBlock():
        add_assign("out_data", [], "0", [])
```

生成的 Verilog 代码：

```verilog
module Test #(
    parameter PARAM_A = 32
) (
);
if (rstn) begin
    assign out_data = in_data;
end
else begin
    assign out_data = 0;
end
endmodule
```

## 特性

- 支持模块定义
- 支持 always 块
- 支持条件语句（if-else）
- 支持循环语句（for）
- 支持生成块（generate）
- 支持变量声明（wire、reg、genvar、integer）
- 支持端口定义（input、output、inout）
- 支持参数定义
- 支持模块实例化

## 许可证

本项目采用 GNU 通用公共许可证第3版（GPLv3）。这意味着你可以自由地：
- 使用
- 修改
- 分发

本软件，但任何修改后的版本都必须以相同的许可证发布。完整的许可证文本请参见 [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.html)。 