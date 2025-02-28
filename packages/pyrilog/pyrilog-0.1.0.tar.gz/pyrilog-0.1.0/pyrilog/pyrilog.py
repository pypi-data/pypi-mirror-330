import enum
import string


class VAR_TYPE(enum.Enum):
    WIRE = "wire"
    REG = "reg"
    GENVAR = "genvar"
    INTERGER = "integer"
    DEFAULT = "default"


class BaseBlock:
    _current_instance_stack = []

    def __init__(self) -> None:
        self.body = []

    def __enter__(self):
        BaseBlock._current_instance_stack.append(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if len(BaseBlock._current_instance_stack) > 1:
            father_block = BaseBlock._current_instance_stack[-2]
            father_block.add_block(self)
        BaseBlock._current_instance_stack.pop()
        if exc_type:
            print(f"An exception of type {exc_type} occurred.")
            print(f"Exception value: {exc_val}")
            print(f"Traceback: {exc_tb}")

    def add_body(self, line: str):
        self.body.append(line)

    def generate(self) -> str:
        return "\n".join(self.body)

    def add_block(self, block):
        self.add_body(block.generate())


class ModuleBlock(BaseBlock):
    def __init__(self, module_name: str):
        super().__init__()
        self.module_name = module_name
        self.parameters = []
        self.inputs = []
        self.outputs = []
        self.inouts = []

    def generate(self) -> str:
        module_text = f"module {self.module_name} #(\n"
        params = ",\n".join(self.parameters)
        inouts = ",\n".join(self.inputs + self.outputs + self.inouts)
        bodys = "\n".join(self.body)
        # 写入 parameter
        module_text += params
        module_text += "\n) (\n"
        # 写入 inout
        module_text += inouts
        module_text += "\n);\n"
        # 写入 body
        module_text += bodys
        module_text += "\nendmodule"
        return module_text


class AlwaysBlock(BaseBlock):
    def __init__(self, sensitivity: str = "posedge clk") -> None:
        super().__init__()
        self.sensitivity = sensitivity

    def generate(self) -> str:
        generate_lines = []
        generate_lines.append(f"always @({self.sensitivity}) begin")
        generate_lines.extend(self.body)
        generate_lines.append("end")
        return "\n".join(generate_lines)


class IfBlock(BaseBlock):
    def __init__(self, condition: str = "rstn") -> None:
        super().__init__()
        self.condition = condition

    def generate(self) -> str:
        generate_lines = []
        generate_lines.append(f"if ({self.condition}) begin")
        generate_lines.extend(self.body)
        generate_lines.append("end")
        return "\n".join(generate_lines)


class ForBlock(BaseBlock):
    def __init__(
        self, initial: str, condition: str, update: str, tag: str = ""
    ) -> None:
        super().__init__()
        self.initial = initial
        self.update = update
        self.condition = condition
        self.tag = tag

    def generate(self) -> str:
        generate_lines = []
        if self.tag:
            generate_lines.append(
                f"for ({self.initial}; {self.condition}; {self.update}) begin : {self.tag}"
            )
        else:
            generate_lines.append(
                f"for ({self.initial}; {self.condition}; {self.update}) begin"
            )
        generate_lines.extend(self.body)
        generate_lines.append("end")
        return "\n".join(generate_lines)


class ElseBlock(BaseBlock):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> str:
        generate_lines = []
        generate_lines.append("else begin")
        generate_lines.extend(self.body)
        generate_lines.append("end")
        return "\n".join(generate_lines)


class GenerateBlock(BaseBlock):
    def __init__(self) -> None:
        super().__init__()

    def generate(self) -> str:
        generate_lines = []
        generate_lines.append("generate")
        generate_lines.extend(self.body)
        generate_lines.append("endgenerate")
        return "\n".join(generate_lines)


class VerilogGenerator(BaseBlock):
    def __init__(self) -> None:
        super().__init__()


class _VerilogSentence:
    @staticmethod
    def parameter_sentence(name: str, value: str) -> str:
        return f"parameter {name} = {value}"

    @staticmethod
    def input_sentence(
        var_type: VAR_TYPE = VAR_TYPE.DEFAULT,
        name: str = "",
        width: str = "1",
        height: str = "1",
    ) -> str:
        input_template = string.Template("input $var_type$width$name$height")
        if var_type == VAR_TYPE.DEFAULT:
            var_type = ""
        else:
            var_type = f"{var_type} "
        if width == "1":
            width = ""
        else:
            width = f"[{width} - 1 : 0] "
        if height == "1":
            height = ""
        else:
            height = f"[{height} - 1 : 0]"
        input_sentence = input_template.substitute(
            var_type=var_type, width=width, name=name, height=height
        )
        return input_sentence

    @staticmethod
    def output_sentence(
        var_type: VAR_TYPE, name: str, width: str = "1", height: str = "1"
    ):
        output_template = string.Template("output $var_type$width$name$height")
        if var_type == VAR_TYPE.DEFAULT:
            var_type = ""
        else:
            var_type = f"{var_type} "
        if width == "1":
            width = ""
        else:
            width = f"[{width} - 1 : 0] "
        if height == "1":
            height = ""
        else:
            height = f"[{height} - 1 : 0]"
        output_sentence = output_template.substitute(
            var_type=var_type, width=width, name=name, height=height
        )
        return output_sentence

    @staticmethod
    def inout_sentence(
        var_type: VAR_TYPE, name: str, width: str = "1", height: str = "1"
    ):
        inout_template = string.Template("inout $var_type$width$name$height")
        if var_type == VAR_TYPE.DEFAULT:
            var_type = ""
        else:
            var_type = f"{var_type} "
        if width == "1":
            width = ""
        else:
            width = f"[{width} - 1 : 0] "
        if height == "1":
            height = ""
        else:
            height = f"[{height} - 1 : 0]"
        inout_sentence = inout_template.substitute(
            var_type=var_type, width=width, name=name, height=height
        )
        return inout_sentence

    @staticmethod
    def assign_sentence(
        out_var: str, out_indices: list, in_var: str, in_indexs: list
    ) -> str:
        assign_template = string.Template(
            "assign $out_var$out_indices = $in_var$in_indices;"
        )
        out_indices_str = "".join([f"[{index}]" for index in out_indices])
        in_indices_str = "".join([f"[{index}]" for index in in_indexs])
        assign_sentence = assign_template.substitute(
            out_var=out_var,
            out_indices=out_indices_str,
            in_var=in_var,
            in_indices=in_indices_str,
        )
        return assign_sentence

    @staticmethod
    def instance_sentence(
        module_name: str, instance_name: str, parameters: dict, ports: dict
    ) -> str:
        instance_lines = [f"{module_name} "]
        if parameters:
            instance_lines = [f"{module_name} #("]
            for param_name, param_value in parameters.items():
                instance_lines.append(f"    .{param_name}({param_value}),")
            if instance_lines[-1].endswith(","):
                instance_lines[-1] = instance_lines[-1][:-1]
            instance_lines.append(")")
        instance_lines.append(f"{instance_name} (")
        for port_name, signal_name in ports.items():
            instance_lines.append(f"    .{port_name}({signal_name}),")
        if instance_lines[-1].endswith(","):
            instance_lines[-1] = instance_lines[-1][:-1]
        instance_lines.append(");")
        return "\n".join(instance_lines)

    @staticmethod
    def var_sentence(
        var_type: VAR_TYPE, name: str, width: str = "1", height: str = "1"
    ) -> str:
        var_template = string.Template("$var_type $width$name$height;")
        if width == "1":
            width = ""
        else:
            width = f"[{width} - 1 : 0] "
        if height == "1":
            height = ""
        else:
            height = f"[{height} - 1 : 0]"
        var_sentence = var_template.substitute(
            var_type=var_type.value, width=width, name=name, height=height
        )
        return var_sentence


def _find_father() -> BaseBlock:
    return BaseBlock._current_instance_stack[-1]


def add_body(line: str):
    father = _find_father()
    father.add_body(line)


def add_newline():
    add_body("")


def add_parameter(name: str, value: str):
    father = _find_father()
    try:
        assert father.__class__ == ModuleBlock
        father.parameters.append(_VerilogSentence.parameter_sentence(name, value))
    except Exception as e:
        raise e


def add_input(
    name: str,
    width: str = "1",
    height: str = "1",
    var_type: VAR_TYPE = VAR_TYPE.DEFAULT,
):
    father = _find_father()
    try:
        assert father.__class__ == ModuleBlock
        father.inputs.append(
            _VerilogSentence.input_sentence(var_type, name, str(width), str(height))
        )
    except Exception as e:
        raise e


def add_output(
    name: str,
    width: str = "1",
    height: str = "1",
    var_type: VAR_TYPE = VAR_TYPE.DEFAULT,
):
    father = _find_father()
    try:
        assert father.__class__ == ModuleBlock
        father.outputs.append(
            _VerilogSentence.output_sentence(var_type, name, str(width), str(height))
        )
    except Exception as e:
        raise e


def add_inout(
    name: str,
    width: str = "1",
    height: str = "1",
    var_type: VAR_TYPE = VAR_TYPE.DEFAULT,
):
    father = _find_father()
    try:
        assert father.__class__ == ModuleBlock
        father.inouts.append(
            _VerilogSentence.inout_sentence(var_type, name, str(width), str(height))
        )
    except Exception as e:
        raise e


def add_assign(out_var: str, out_indices: list, in_var: str, in_indexs: list):
    father = _find_father()
    father.add_body(
        _VerilogSentence.assign_sentence(out_var, out_indices, in_var, in_indexs)
    )


def add_instance(module_name: str, instance_name: str, parameters: dict, ports: dict):
    father = _find_father()
    father.add_body(
        _VerilogSentence.instance_sentence(
            module_name, instance_name, parameters, ports
        )
    )


def add_var(var_type: VAR_TYPE, name: str, width: str = "1", height: str = "1"):
    father = _find_father()
    father.add_body(_VerilogSentence.var_sentence(var_type, name, width, height))


def add_wire(name: str, width: str = "1", height: str = "1"):
    add_var(VAR_TYPE.WIRE, name, width, height)


def add_reg(name: str, width: str = "1", height: str = "1"):
    add_var(VAR_TYPE.REG, name, width, height)


def add_genvar(name: str):
    add_var(VAR_TYPE.GENVAR, name)


def add_integer(name: str):
    add_var(VAR_TYPE.INTERGER, name)


def _test_generate():
    with VerilogGenerator() as generator:
        with ModuleBlock("Test"):
            add_parameter("adsa", "dsa")
            with IfBlock("rstn"):
                add_assign("a", [], "b", [])
            with ElseBlock():
                add_assign("a", [], "c", [])
        with ModuleBlock("Test11"):
            add_parameter("adsa", "dsa")
            with IfBlock("rstn"):
                add_assign("a", [], "b", [])
            with ElseBlock():
                add_assign("a", [], "c", [])

    print(len(generator.body))
    with open("test.sv", "w") as f:
        f.write(generator.generate())


if __name__ == "__main__":
    _test_generate()
