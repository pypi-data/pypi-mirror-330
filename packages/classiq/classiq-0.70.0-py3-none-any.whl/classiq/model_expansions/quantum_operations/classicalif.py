from collections.abc import Sequence

from classiq.interface.debug_info.debug_info import new_function_debug_info_by_node
from classiq.interface.model.classical_if import ClassicalIf
from classiq.interface.model.quantum_function_call import QuantumFunctionCall
from classiq.interface.model.quantum_statement import QuantumStatement

from classiq.model_expansions.closure import FunctionClosure
from classiq.model_expansions.quantum_operations.call_emitter import CallEmitter
from classiq.model_expansions.scope import Scope


def _is_all_identity_calls(body: Sequence[QuantumStatement]) -> bool:
    return all(
        isinstance(stmt, QuantumFunctionCall) and stmt.func_name.lower() == "identity"
        for stmt in body
    )


class ClassicalIfEmitter(CallEmitter[ClassicalIf]):
    def emit(self, classical_if: ClassicalIf, /) -> bool:
        condition = self._interpreter.evaluate(classical_if.condition).as_type(bool)
        op_name = "then" if condition else "else"
        is_generative = classical_if.is_generative()

        body: Sequence[QuantumStatement]
        if is_generative:
            if not classical_if.has_generative_block(op_name):
                return True
            context = self._expand_generative_context(classical_if, op_name, op_name)
            context.blocks["body"] = context.blocks[op_name]
            context.blocks.pop(op_name)
            body = context.statements("body")
        else:
            body = classical_if.then if condition else classical_if.else_

        if _is_all_identity_calls(body):
            return True

        if is_generative or not self._should_wrap(body):
            for stmt in body:
                if is_generative:
                    self._interpreter._builder.emit_statement(stmt)
                else:
                    self._interpreter.emit_statement(stmt)
            return True

        then_else_func = FunctionClosure.create(
            name=self._counted_name_allocator.allocate("then" if condition else "else"),
            body=body,
            scope=Scope(parent=self._current_scope),
            lambda_external_vars=self._builder.current_block.captured_vars,
        )
        self._emit_quantum_function_call(
            then_else_func, list(), new_function_debug_info_by_node(classical_if)
        )
        return True
