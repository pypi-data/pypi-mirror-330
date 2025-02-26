"""Create Embeddings via OpenAI embeddings API endpoint"""

import json
import re
from collections.abc import Generator, Sequence
from string import Template

from cmem_plugin_base.dataintegration.context import (
    ExecutionContext,
    ExecutionReport,
)
from cmem_plugin_base.dataintegration.description import Icon, Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities,
    Entity,
    EntityPath,
    EntitySchema,
)
from cmem_plugin_base.dataintegration.parameter.code import JsonCode
from cmem_plugin_base.dataintegration.parameter.multiline import MultilineStringParameterType
from cmem_plugin_base.dataintegration.parameter.password import Password, PasswordParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from cmem_plugin_base.dataintegration.ports import (
    FixedNumberOfInputs,
    FixedSchemaPort,
    FlexibleSchemaPort,
)
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

from cmem_plugin_llm.commons import OpenAPIModel, SamePathError, input_paths_to_list

DEFAULT_INSTRUCTION_OUTPUT_PATH = "_instruction_output"
MODEL_EXAMPLE = "gpt-4o"
INSTRUCTION_EXAMPLE = """Write a paragraph about this entity: ${entity}"""
PROMPT_TEMPLATE_EXAMPLE = JsonCode("""[
    {
        "role": "developer",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "${instruct}"
    }
]""")


@Plugin(
    label="Execute Instructions",
    plugin_id="cmem_plugin_llm-ExecuteInstructions",
    icon=Icon(package=__package__, file_name="execute_instruction.svg"),
    description="Send instructions (prompt) to an LLM and process the result.",
    documentation="""
This plugin allows to execute an LLM instruction over a given list of entities.
After being processed each entity receive one additional path, the ```_instruction_output```.
  - The ```_instruction_output``` path contains the output of the executed instruction over
    the entity.


#### Parameters

- ```url```: openAI compatible endpoint, default ```https://api.openai.com/v1```
- ```model```: embedding model, default ```gpt-o```
- ```api_key```: api key of the endpoint, default blank
- ```timout_single_request```: the request timeout in milliseconds, default ```10000```
- ```instruction_template```: the instruction template
  default instruct template: ```Write a paragraph about this entity: ${entity}```
- ```prompt_template```: the prompt template
  default prompt template:
  ```
              [{
                  "role": "developer",
                  "content": "You are a helpful assistant."
              },
              {
                  "role": "user",
                  "content": "${instruct}"
              }]
  ```
- ```instruct_output_path```: output path that will contain the output of the executed instruction,
  default ```_instruction_output```""",
    parameters=[
        PluginParameter(
            name="url",
            label="URL",
            description="URL of the OpenAI API (without endpoint path and without trailing slash)",
            default_value="https://api.openai.com/v1",
        ),
        PluginParameter(
            name="api_key",
            label="API key",
            param_type=PasswordParameterType(),
            description="Fill the OpenAI API key if needed "
            "(or give a dummy value in case you access an unsecured endpoint).",
        ),
        PluginParameter(
            name="model",
            label="Instruct Model",
            description=f"The instruct model, e.g. {MODEL_EXAMPLE}",
            param_type=OpenAPIModel(),
        ),
        PluginParameter(
            name="instruct_template",
            label="Instruction Template",
            description="A template instruction.",
            default_value=INSTRUCTION_EXAMPLE,
            param_type=MultilineStringParameterType(),
        ),
        PluginParameter(
            name="instruct_paths",
            label="Used entity paths (comma-separated list)",
            description="Changing this value will change, which input paths are used by the "
            "workflow task. A blank value means, all paths are used.",
            advanced=True,
            default_value="",
        ),
        PluginParameter(
            name="timout_single_request",
            label="Timeout",
            description="The timeout of a single request in milliseconds",
            advanced=True,
            default_value=10000,
        ),
        PluginParameter(
            name="prompt_template",
            label="Prompt Template",
            description="""A prompt template compatible with OpenAI chat completion API message
            object.""",
            advanced=True,
            default_value=PROMPT_TEMPLATE_EXAMPLE,
        ),
        PluginParameter(
            name="instruct_output_path",
            label="Instruct Output Path",
            description="The entity path where the instruction result will be writen.",
            advanced=True,
            default_value=DEFAULT_INSTRUCTION_OUTPUT_PATH,
        ),
    ],
)
class ExecuteInstruction(WorkflowPlugin):
    """Execute Instructions from OpenAI completion API endpoint over entities"""

    execution_context: ExecutionContext
    embeddings: OpenAIEmbeddings
    input_paths: Sequence[EntityPath]
    instruct_output_path: str
    instruct_report: ExecutionReport
    prompt_template: str
    instruct_template: str
    client: OpenAI
    model: str

    def __init__(  # noqa: PLR0913
        self,
        url: str,
        api_key: Password | str = "",
        model: str = MODEL_EXAMPLE,
        timout_single_request: int = 10000,
        instruct_paths: str = "",
        instruct_output_path: str = DEFAULT_INSTRUCTION_OUTPUT_PATH,
        prompt_template: JsonCode = PROMPT_TEMPLATE_EXAMPLE,
        instruct_template: str = INSTRUCTION_EXAMPLE,
    ) -> None:
        self.base_url = url
        self.timout_single_request = timout_single_request
        self.api_key = api_key if isinstance(api_key, str) else api_key.decrypt()
        if self.api_key == "":
            self.api_key = "dummy-key"
        self.instruct_path_list = input_paths_to_list(instruct_paths)
        self.instruct_output_path = instruct_output_path
        self.prompt_template = str(prompt_template)
        self.instruct_template = instruct_template
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.instruct_report = ExecutionReport()
        self.instruct_report.operation = "executing"
        self.instruct_report.operation_desc = "instructions executed"
        self._setup_ports()

    @staticmethod
    def template_has_placeholder(content: str) -> bool:
        """Check the existence of placeholders in a given string"""
        pattern = r"\$\{\w+\}"  # Matches ${anything_inside}
        return bool(re.search(pattern, content))

    def _setup_ports(self) -> None:
        """Configure input and output ports depending on the configuration"""
        instruct_output_path = EntityPath(path=self.instruct_output_path)
        if not self.template_has_placeholder(self.instruct_template):
            # no_input_fixed_output
            # no input data used, so input port closed and output port minimal schema
            self.input_ports = FixedNumberOfInputs([])
            output_schema = EntitySchema(type_uri="entity", paths=[instruct_output_path])
            self.output_port = FixedSchemaPort(schema=output_schema)
            return
        if len(self.instruct_path_list) == 0:
            # flexible_in_and_output
            # empty path list means, the complete entity is used and extended
            # single input port with flexible schema
            self.input_ports = FixedNumberOfInputs([FlexibleSchemaPort()])
            self.output_port = FlexibleSchemaPort()
        else:
            # fixed_input_fixed_output
            # path list set, so we know the input schema (and derive the output schema)
            input_paths = [EntityPath(path=_) for _ in self.instruct_path_list]
            input_schema = EntitySchema(type_uri="entity", paths=input_paths)
            self.input_ports = FixedNumberOfInputs(ports=[FixedSchemaPort(schema=input_schema)])
            output_paths = input_paths.copy()
            output_paths.append(instruct_output_path)
            output_schema = EntitySchema(type_uri="entity", paths=output_paths)
            self.output_port = FixedSchemaPort(schema=output_schema)

    def _generate_output_schema(self, input_schema: EntitySchema) -> EntitySchema:
        """Get output schema"""
        paths = list(input_schema.paths).copy()
        paths.append(EntityPath(self.instruct_output_path))
        return EntitySchema(type_uri=input_schema.type_uri, paths=paths)

    def _cancel_workflow(self) -> bool:
        """Cancel workflow"""
        try:
            if self.execution_context.workflow.status() == "Canceling":
                self.log.info("End task (Cancelled Workflow).")
                return True
        except AttributeError:
            pass
        return False

    def _instruct_report_update(self, n: int) -> None:
        """Update report"""
        if hasattr(self.execution_context, "report"):
            self.instruct_report.entity_count += n
            self.execution_context.report.update(self.instruct_report)

    @staticmethod
    def _entity_to_dict(paths: Sequence[EntityPath], entity: Entity) -> dict[str, list[str]]:
        """Create a dict representation of an entity"""
        entity_dic = {}
        for key, value in zip(paths, entity.values, strict=False):
            entity_dic[key.path] = list(value)
        return entity_dic

    @staticmethod
    def _template_fill(template: str, variable: str, value: str) -> str:
        """Fill the template replacing the variable by the given value"""
        variable_map: dict = {}
        variable_map[variable] = value
        return Template(template).safe_substitute(variable_map)

    def _process_entities(self, entities: Entities) -> Generator[Entity]:
        """Process the entities, yielding new entity objects"""
        entity: Entity
        self.input_paths: Sequence[EntityPath] = entities.schema.paths
        if len(self.instruct_path_list) > 0:
            self.input_paths = [EntityPath(path=_) for _ in self.instruct_path_list]
        self._instruct_report_update(0)
        for entity in entities.entities:
            entity_dict = self._entity_to_dict(self.input_paths, entity)
            instruct: str = self._template_fill(
                self.instruct_template, "entity", json.dumps(entity_dict)
            )
            messages = json.loads(self.prompt_template)
            instruction = messages[1]["content"]
            instruction_user: str = self._template_fill(instruction, "instruct", instruct)
            messages[1]["content"] = instruction_user
            completion = self.client.chat.completions.create(model=self.model, messages=messages)
            entity_dict[self.instruct_output_path] = [completion.choices[0].message.content or ""]
            values = list(entity_dict.values())
            self._instruct_report_update(1)
            if self._cancel_workflow():
                break
            yield Entity(uri=entity.uri, values=values)

    def execute(
        self,
        inputs: Sequence[Entities],
        context: ExecutionContext,
    ) -> Entities:
        """Run the workflow operator."""
        self.log.info("Start")
        self.execution_context = context
        try:
            first_input: Entities = inputs[0]
        except IndexError:
            # if we have no input, we create a single input with a Null entity
            first_input = Entities(
                entities=iter([Entity(uri="urn:x-ecc:null", values=[])]),
                schema=EntitySchema(type_uri="urn:x-ecc:null-type", paths=[]),
            )
        if self.instruct_output_path in [_.path for _ in first_input.schema.paths]:
            raise SamePathError(self.instruct_output_path)
        entities = self._process_entities(first_input)
        schema = self._generate_output_schema(first_input.schema)
        self.log.info("End")
        return Entities(entities=entities, schema=schema)
