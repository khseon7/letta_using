### 필요 applications
- <a href="https://docs.letta.com/install">letta Desktop</a> 다운
- Docker를 사용하여 만든 Local Agent 확인하려면 `docker run ...` 명령어를 키고, <a href="https://app.letta.com/">local server</a>에 들어가면 확인할 수 있다.
- letta의 기본 Reference: <a href="https://github.com/letta-ai/letta-python/blob/main/reference.md">letta Python SDK</a>
- <a href="https://github.com/letta-ai/letta/tree/main/examples">letta-Examples</a>

### docker 명령어(이 경우는 local agent를 만들때 사용하니 굳이 실행하지 않아도 된다!)
``` shell
docker run \
  -v ~/.letta/.persist/pgdata:/var/lib/postgresql/data \
  -p 8283:8283 \
  -e OPENAI_API_KEY="your_openai_api_key" \
  letta/letta:latest
```

자세한 내용은 <a href="https://github.com/letta-ai/letta">memGPT 공식 GitHub 사이트</a>에서 확인하면 된다.
