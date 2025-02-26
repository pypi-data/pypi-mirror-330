# # 启动 Node.js 子进程
# node_process = subprocess.Popen(
#     ['node', 'script.js'],
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
#     stderr=subprocess.STDOUT,
#     universal_newlines=True,
#     encoding='utf-8'
# )


# try:
#     while True:
#         # 获取用户输入
#         user_input = input("请输入数据 (输入 'exit' 来退出): ")
#         # 如果输入是 "exit"，则退出循环并关闭子进程
#         if user_input.strip().lower() == 'exit':
#             break
#
#         # 向 Node.js 子进程发送输入
#         node_process.stdin.write(user_input + '\n')
#         node_process.stdin.flush()  # 刷新stdin缓冲区，确保数据被写入
#
#         while True:
#             output = node_process.stdout.readline()  # 读取子进程的输出
#             if output[:10] != "[[result]]":
#                 continue
#             break
#
#         print(json.loads(output.strip()[10:]))
#
# finally:
#     # 关闭子进程
#     print('关闭子进程')
#     node_process.stdin.close()
#     print(node_process.stdout.read())
#     node_process.stdout.close()
#     node_process.stderr.close()
#     node_process.terminate()
#     node_process.wait()  # 等待子进程结束
#     print(node_process)
