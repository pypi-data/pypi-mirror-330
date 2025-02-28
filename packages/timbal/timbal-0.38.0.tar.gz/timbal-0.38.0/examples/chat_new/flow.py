from timbal import Flow


flow = (
    Flow()
    .add_llm(model="gpt-4o-mini")
    .set_data_map("llm.prompt", "prompt")
    .set_output("response", "llm.return")
    .compile()
)
