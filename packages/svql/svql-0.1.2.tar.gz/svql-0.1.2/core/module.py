import pyslang
import pandas as pd
import pandasql
from ast_visitors import port_visitor, param_visitor, submodule_inst_visitor
from utils import attr_utils 

class Module:
    def __init__(self, file_paths: List[str]):
        self.file_paths = file_paths
        self.asts = [pyslang.SyntaxTree.fromFile(file_path) for file_path in file_paths]
        self.module = self.ast.root.members[0]

        # Module properties
        self.name = self.module.header.name.value        
        self.params = pd.DataFrame(columns=[
            "name", "dtype", "default_value", 
            "override_value", "scope", "typed_param"
        ])
        self.ports = pd.DataFrame(columns=[
            "name", "dtype", "width", "direction", "connected_to"
        ])
        self.tables = {
            "params": self.params,
            "ports": self.ports
        }

        # Build all tables
        self.build()

    def build(self) -> None:
        self._build_params()
        self._build_ports()
        self._build_submodule_instances()
        self._update_tables()

    def _build_params(self) -> None:
        root = self.module.header.parameters.declarations
        visitor = param_visitor.ParamVisitor()
        
        for decl in root: visitor.visit(decl)

        self.params = pd.DataFrame(visitor.params)

    def _build_ports(self) -> None:
        root = self.module.header.ports.ports
        visitor = port_visitor.PortVisitor()

        for port in root: visitor.visit(port)

        self.ports = pd.DataFrame(visitor.ports)

    def _build_submodule_instances(self) -> None:
        root = self.module.members
        visitor = submodule_inst_visitor.SubmoduleInstanceVisitor()

        for member in root: visitor.visit(member)


        pass

    def _update_tables(self) -> None:
        self.tables["params"] = self.params
        self.tables["ports"] = self.ports

    query = lambda self, q: pandasql.sqldf(q, self.tables)

    def print(self) -> None:
        print("Module: ", self.name)
        print("Parameters: \n", self.params)
        print("Ports: \n", self.ports)

    

