def render_html_content(report_data: dict, mode: str = "real-time") -> str:
    """
    优化版九宫格紧凑布局 · 自动生成热点新闻HTML
    一屏显示更多内容，不再无限下滑
    """
    import time

    current_time = time.strftime("%m-%d %H:%M", time.localtime())
    total_titles = 0
    hot_news_count = 0

    if "stats" in report_data:
        for stat in report_data["stats"]:
            hot_news_count += len(stat.get("titles", []))

    for platform_data in report_data.get("platform_data", []):
        total_titles += len(platform_data.get("titles", []))

    report_type = {
        "daily": "全天汇总",
        "hourly": "小时汇总",
        "real-time": "实时榜单"
    }.get(mode, "实时榜单")

    # ======================
    # 🔥 核心：九宫格紧凑布局
    # ======================
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>热点新闻分析 - 优化版</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        :root {{
            --primary: #4f46e5;
            --primary-light: #7c3aed;
            --danger: #dc2626;
            --warning: #ea580c;
            --success: #059669;
            --gray-100: #f8f9fa;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-600: #6b7280;
            --gray-800: #1f2937;
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
            --radius-sm: 6px;
            --radius-md: 12px;
            --radius-full: 9999px;
            --transition: all 0.2s ease;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #fafafa;
            color: var(--gray-800);
            line-height: 1.5;
            padding: 0;
            margin: 0;
        }}

        .container {{
            max-width: 1200px;
            margin: 20px auto;
            background: white;
            border-radius: var(--radius-md);
            overflow: hidden;
            box-shadow: var(--shadow-md);
        }}

        .header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
            color: white;
            padding: 24px;
            position: relative;
        }}

        .save-buttons {{
            position: absolute;
            top: 16px;
            right: 16px;
            display: flex;
            gap: 8px;
        }}

        .save-btn {{
            background: rgba(255,255,255,0.2);
            border: 1px solid rgba(255,255,255,0.3);
            color: white;
            padding: 6px 12px;
            border-radius: var(--radius-sm);
            font-size: 12px;
            cursor: pointer;
        }}

        .header-title {{
            font-size: 22px;
            font-weight: 700;
            text-align: center;
            margin-bottom: 16px;
        }}

        .header-info {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            font-size: 14px;
        }}

        .info-item {{
            text-align: center;
            background: rgba(255,255,255,0.1);
            padding: 8px;
            border-radius: var(--radius-sm);
        }}

        .info-label {{
            font-size: 12px;
            opacity: 0.8;
        }}

        .content {{
            padding: 20px;
        }}

        /* 🔥 九宫格核心布局 */
        .news-list {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
        }}

        .word-group {{
            margin-bottom: 30px;
        }}

        .word-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--gray-200);
        }}

        .word-name {{
            font-size: 16px;
            font-weight: 600;
        }}

        .word-count {{
            font-size: 12px;
            padding: 3px 8px;
            border-radius: 999px;
            background: rgba(220,38,38,0.1);
            color: var(--danger);
        }}

        /* 🔥 紧凑卡片 */
        .news-item {{
            background: var(--gray-100);
            border-radius: var(--radius-sm);
            padding: 12px;
            transition: var(--transition);
        }}

        .news-item:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-sm);
            background: white;
        }}

        .news-title {{
            font-size: 14px;
            line-height: 1.4;
            color: var(--gray-800);
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            margin-bottom: 6px;
        }}

        .news-link {{
            text-decoration: none;
            color: inherit;
        }}

        .news-header {{
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--gray-600);
        }}

        .source-name {{
            background: white;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid var(--gray-200);
        }}

        .rank-num {{
            background: var(--danger);
            color: white;
            padding: 1px 6px;
            border-radius: 999px;
            font-size: 10px;
            font-weight: bold;
        }}

        .footer {{
            padding: 16px;
            background: var(--gray-100);
            text-align: center;
            font-size: 12px;
            color: var(--gray-600);
        }}

        /* 响应式 */
        @media (max-width: 768px) {{
            .news-list {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .header-info {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media (max-width: 480px) {{
            .news-list {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <div class="save-buttons">
            <button class="save-btn" onclick="saveAsImage()">保存为图片</button>
        </div>
        <div class="header-title">热点新闻分析</div>
        <div class="header-info">
            <div class="info-item"><span class="info-label">报告类型</span><br>{report_type}</div>
            <div class="info-item"><span class="info-label">新闻总数</span><br>{total_titles} 条</div>
            <div class="info-item"><span class="info-label">热点新闻</span><br>{hot_news_count} 条</div>
            <div class="info-item"><span class="info-label">生成时间</span><br>{current_time}</div>
        </div>
    </div>

    <div class="content">
"""

    # 渲染热点分组
    if "stats" in report_data and report_data["stats"]:
        for idx, stat in enumerate(report_data["stats"]):
            word = stat.get("word", "未命名分类")
            count = stat.get("count", 0)
            titles = stat.get("titles", [])

            html += f"""
        <div class="word-group">
            <div class="word-header">
                <div>
                    <span class="word-name">{word}</span>
                    <span class="word-count">{count} 条</span>
                </div>
                <div style="font-size:12px;color:#888">{idx+1}/{len(report_data["stats"])}</div>
            </div>
            <div class="news-list">
            """

            for i, title_data in enumerate(titles[:15]):  # 最多显示15条，避免过长
                title = title_data.get("title", "")
                url = title_data.get("url", "#")
                source = title_data.get("source_name", "未知")
                rank = title_data.get("ranks", [0])[0] if title_data.get("ranks") else 0

                html += f"""
                <div class="news-item">
                    <a href="{url}" target="_blank" class="news-link">
                        <div class="news-title">{title}</div>
                    </a>
                    <div class="news-header">
                        <span class="source-name">{source}</span>
                        <span class="rank-num">{rank}</span>
                    </div>
                </div>
                """

            html += """
            </div>
        </div>
        """

    # 底部
    html += """
    </div>
    <div class="footer">
        热点雷达 · 数据自动生成 · 仅供参考
    </div>
</div>

<script>
function saveAsImage() {
    const container = document.querySelector('.container');
    html2canvas(container, { scale: 2, useCORS: true }).then(canvas => {
        const link = document.createElement('a');
        link.download = '热点新闻_' + new Date().getTime() + '.png';
        link.href = canvas.toDataURL('image/png');
        link.click();
    });
}
</script>

</body>
</html>
"""

    return html
