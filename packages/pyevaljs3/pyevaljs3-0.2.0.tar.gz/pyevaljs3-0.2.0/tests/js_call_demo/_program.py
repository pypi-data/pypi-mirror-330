NODE_PROGRAM = """
var __process = process;
{source};
__process.stdin.setEncoding('utf8');
__process.stdin.on('data', function(data) {{
    let input = data.trim();
    try {{
        var res = eval(input)
        console.log('[[<<result>>]]' + JSON.stringify(res))
    }} catch (e) {{
        console.log('[[<<exception>>]]' + JSON.stringify(e.stack))
    }}
}});
"""
