import re
from typing import Dict, Any, List, Tuple
import os
from jarvis.jarvis_agent.output_handler import OutputHandler
from jarvis.jarvis_tools.git_commiter import GitCommitTool
from jarvis.jarvis_tools.read_code import ReadCodeTool
from jarvis.jarvis_utils import OutputType, PrettyOutput, get_multiline_input, has_uncommitted_changes, user_confirm


class PatchOutputHandler(OutputHandler):
    def name(self) -> str:
        return "PATCH"

    def handle(self, response: str) -> Tuple[bool, Any]:
        return False, apply_patch(response)
    
    def can_handle(self, response: str) -> bool:
        if _parse_patch(response):
            return True
        return False
    
    def prompt(self) -> str:
        return """
# 🛠️ Code Patch Specification
When making changes, you MUST:
1. Explain each modification BEFORE the <PATCH> block using:
   # [OPERATION] on [FILE]: Lines X-Y
   # Reason: [CLEAR EXPLANATION]
2. Maintain original code style and compatibility:
   - Preserve existing indentation levels
   - Keep surrounding empty lines
   - Match variable naming conventions
   - Maintain API compatibility
3. Follow the exact patch format below
4. Use separate <PATCH> blocks for different files
5. Include ONLY modified lines in content

<PATCH>
File path [Range]
Code content
</PATCH>

Critical Rules:
- NEVER include unchanged code in patch content
- ONLY show lines that are being modified/added
- Maintain original line breaks around modified sections
- Preserve surrounding comments unless explicitly modifying them

Examples:
# ======== REPLACE ========
# GOOD: Only modified lines
# REPLACE in src/app.py: Lines 5-8
# Reason: Update calculation formula
<PATCH>
src/app.py [5,8]
    result = (base_value * 1.15) + tax
    logger.debug("New calculation applied")
</PATCH>

# BAD: Includes unchanged lines
<PATCH>
src/app.py [5,8]
def calculate():
    # Original comment (should not be included)
    result = (base_value * 1.15) + tax
    return result  # Original line
</PATCH>

# ======== INSERT ========
# GOOD: Insert single line
# INSERT in utils/logger.py: Before line 3 
# Reason: Add initialization check
<PATCH>
utils/logger.py [3]
if not _initialized: initialize()
</PATCH>

# BAD: Extra empty lines
<PATCH>
utils/logger.py [3]

if not _initialized: 
    initialize()

</PATCH>

# ======== NEW FILE ========
# GOOD: Complete minimal content
# NEW FILE in config/settings.yaml: Create new config
<PATCH>
config/settings.yaml [1]
database:
  host: localhost
  port: 5432
</PATCH>

# BAD: Placeholder content
<PATCH>
config/settings.yaml [1]
TODO: Add configuration
</PATCH>

# ======== DELETE ========
# GOOD: Empty content for deletion
# DELETE in src/old.py: Lines 10-12 
# Reason: Remove deprecated function
<PATCH>
src/old.py [10,12]
</PATCH>

# BAD: Comment in delete operation
<PATCH>
src/old.py [10,12]
# Remove these lines
</PATCH>
"""


def _parse_patch(patch_str: str) -> Dict[str, List[Dict[str, Any]]]:
    """解析补丁格式"""
    result = {}
    header_pattern = re.compile(
        r'^\s*"?(.+?)"?\s*\[(\d+)(?:,(\d+))?\]\s*$'  # Match file path and line number
    )
    patches = re.findall(r'<PATCH>\n?(.*?)\n?</PATCH>', patch_str, re.DOTALL)
    
    for patch in patches:
        # 分割首行和内容
        parts = patch.split('\n', 1)
        if len(parts) < 1:
            continue
        header_line = parts[0].strip()
        content = parts[1] if len(parts) > 1 else ''
        
        # 仅在内容非空时添加换行符
        if content and not content.endswith('\n'):
            content += '\n'
            
        # 解析文件路径和行号
        header_match = header_pattern.match(header_line)
        if not header_match:
            continue

        filepath = header_match.group(1)
        start = int(header_match.group(2))       # 保持1-based行号
        end = int(header_match.group(3)) + 1 if header_match.group(3) else start

        # 存储参数
        if filepath not in result:
            result[filepath] = []
        result[filepath].append({
            'filepath': filepath,
            'start': start,
            'end': end,
            'content': content  # 保留原始内容（可能为空）
        })
    for filepath in result.keys():
        result[filepath] = sorted(result[filepath], key=lambda x: x['start'], reverse=True)
    return result


def apply_patch(output_str: str) -> str:
    """Apply patches to files"""
    try:
        patches = _parse_patch(output_str)
    except Exception as e:
        PrettyOutput.print(f"解析补丁失败: {str(e)}", OutputType.ERROR)
        return ""

    ret = ""
    
    for filepath, patch_list in patches.items():
        for patch in patch_list:
            try:
                handle_code_operation(filepath, patch)
                PrettyOutput.print(f"成功处理 操作", OutputType.SUCCESS)
            except Exception as e:
                PrettyOutput.print(f"操作失败: {str(e)}", OutputType.ERROR)
    
    if has_uncommitted_changes():
        diff = get_diff()
        if handle_commit_workflow(diff):
            ret += "Successfully applied the patch\n"
            # Get modified line ranges
            modified_ranges = get_modified_line_ranges()
            modified_code = ReadCodeTool().execute({"files": [{"path": filepath, "start_line": start, "end_line": end} for filepath, (start, end) in modified_ranges.items()]})
            if modified_code["success"]:
                ret += "New code:\n"
                ret += modified_code["stdout"]
        else:
            ret += "User rejected the patch\nThis is your patch preview:\n"
            ret += diff
        user_input = get_multiline_input("你可以继续输入（输入空行重试，Ctrl+C退出）: ")
        if user_input:
            ret += "\n" + user_input
        else:
            ret = ""

    return ret  # Ensure a string is always returned

def get_diff() -> str:
    """使用更安全的subprocess代替os.system"""
    import subprocess
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        result = subprocess.run(
            ['git', 'diff', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    finally:
        subprocess.run(['git', 'reset', 'HEAD'], check=True)

def handle_commit_workflow(diff:str)->bool:
    """Handle the git commit workflow and return the commit details.
    
    Returns:
        tuple[bool, str, str]: (continue_execution, commit_id, commit_message)
    """
    if not user_confirm("是否要提交代码？", default=True):
        import subprocess
        subprocess.run(['git', 'reset', 'HEAD'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'checkout', '--', '.'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'clean', '-fd'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return False

    git_commiter = GitCommitTool()
    commit_result = git_commiter.execute({})
    return commit_result["success"]

def get_modified_line_ranges() -> Dict[str, Tuple[int, int]]:
    """Get modified line ranges from git diff for all changed files.
    
    Returns:
        Dictionary mapping file paths to tuple with (start_line, end_line) ranges
        for modified sections. Line numbers are 1-based.
    """
    # Get git diff for all files
    diff_output = os.popen("git show").read()
    
    # Parse the diff to get modified files and their line ranges
    result = {}
    current_file = None
    
    for line in diff_output.splitlines():
        # Match lines like "+++ b/path/to/file"
        file_match = re.match(r"^\+\+\+ b/(.*)", line)
        if file_match:
            current_file = file_match.group(1)
            continue
            
        # Match lines like "@@ -100,5 +100,7 @@" where the + part shows new lines
        range_match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", line)
        if range_match and current_file:
            start_line = int(range_match.group(1))  # Keep as 1-based
            line_count = int(range_match.group(2)) if range_match.group(2) else 1
            end_line = start_line + line_count - 1
            result[current_file] = (start_line, end_line)
    
    return result
# New handler functions below ▼▼▼

def handle_new_file(filepath: str, patch: Dict[str, Any]):
    """统一参数格式处理新文件"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(patch['content'])

def handle_code_operation(filepath: str, patch: Dict[str, Any]):
    """处理紧凑格式补丁"""
    try:
        # 新建文件时强制覆盖
        os.makedirs(os.path.dirname(filepath) or '.', exist_ok=True)
        if not os.path.exists(filepath):
            open(filepath, 'w', encoding='utf-8').close()
        with open(filepath, 'r+', encoding='utf-8') as f:
            lines = f.readlines()
            
            new_lines = validate_and_apply_changes(
                lines,
                patch['start'],
                patch['end'],
                patch['content']
            )
            
            f.seek(0)
            f.writelines(new_lines)
            f.truncate()

        PrettyOutput.print(f"成功更新 {filepath}", OutputType.SUCCESS)

    except Exception as e:
        PrettyOutput.print(f"操作失败: {str(e)}", OutputType.ERROR)

def validate_and_apply_changes(
    lines: List[str],
    start: int,
    end: int,
    content: str
) -> List[str]:

    new_content = content.splitlines(keepends=True)
    
    # 插入操作处理
    if start == end:
        if start < 1 or start > len(lines)+1:
            raise ValueError(f"无效插入位置: {start}")
        # 在指定位置前插入
        return lines[:start-1] + new_content + lines[start-1:]
    
    # 范围替换/删除操作
    if start > end:
        raise ValueError(f"起始行{start}不能大于结束行{end}")
    
    max_line = len(lines)
    # 自动修正行号范围
    start = max(1, min(start, max_line+1))
    end = max(start, min(end, max_line+1))
    
    # 执行替换
    return lines[:start-1] + new_content + lines[end-1:]
