from letta_client import Letta, MessageCreate, TextContent
import yaml

# Letta 클라이언트 초기화
client = Letta(base_url="http://localhost:8283")

# 사용하고자 하는 에이전트 이름
tools_name = 'anthropic_agent'

# 에이전트 정보 로드 함수
def load_agent_info(tools_name):
    with open('agent_info.yaml', 'r') as f:
        agent_info = yaml.safe_load(f)

    agent_id = agent_info[tools_name]['agent_id']
    agent_name = agent_info[tools_name]['name']
    agent_description = agent_info[tools_name]['description']
    agent_model = agent_info[tools_name]['model']
    agent_embedding = agent_info[tools_name]['embedding']
    agent_embedding_config = agent_info[tools_name]['embedding_config']
    agent_system = agent_info[tools_name]['system']
    agent_max_tokens = agent_info[tools_name]['max_tokens']
    agent_context_window_limit = agent_info[tools_name]['context_window_limit']

    return agent_id, agent_name, agent_description, agent_model, agent_embedding, agent_embedding_config, agent_system, agent_max_tokens, agent_context_window_limit

# 에이전트 정보 로드
agent_info = load_agent_info(tools_name)
agent_id = agent_info[0]

# 에이전트 조회 및 생성
try:
    agent = client.agents.retrieve(agent_id=agent_id)
    print(f"기존 에이전트를 찾았습니다.")
except Exception as e:
    print(f"새로운 에이전트를 생성합니다.")

    # 에이전트 생성
    new_agent = client.agents.create(
        name=agent_info[1],
        description=agent_info[2],
        model=agent_info[3],
        embedding=agent_info[4],
        embedding_config=agent_info[5],
        include_base_tools=True,
        include_multi_agent_tools=True,
        include_base_tool_rules=True,
        system=agent_info[6],
        max_tokens=agent_info[7],
        context_window_limit=agent_info[8]
    )

    agent_id = new_agent.id

    # agent_info.yaml에 ID 업데이트
    with open('agent_info.yaml', 'r') as f:
        agent_info = yaml.safe_load(f)
    
    agent_info[tools_name]['agent_id'] = agent_id

    with open('agent_info.yaml', 'w') as f:
        yaml.dump(agent_info, f, allow_unicode=True)

# 대화 루프
while True:
    user_input = input("User(exit to quit): ")
    if user_input.lower() == 'exit':
        break

    response = client.agents.messages.create_stream(
        agent_id=agent_id,
        messages=[
            MessageCreate(
                role="user",
                content=[
                    TextContent(
                        text=user_input,
                    )
                ],
            )
        ],
    )

    for idx, chunk in enumerate(response):
        '''
        idx 0: reasoning
        idx 1: response content
        idx 2: usage_metadata
        '''
        if idx == 0:
            print(f"chunk {idx} Reasoning content: {chunk.reasoning}")
        elif idx == 1:
            print(f"chunk {idx} Response content: {chunk.content}")
