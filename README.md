## 界面

![image](image.png)

## 打包
```bash
nuitka --onefile  --standalone --show-memory --show-progress --nofollow-imports --output-dir=out --windows-disable-console --enable-plugin=tk-inter .\remove_dup_jpg.py
```
