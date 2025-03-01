from loguru import logger

if __name__ == "__main__":
    import sys
    # logger.remove()  # 移除默认的日志处理器
    # logger.add(sys.stderr, level="INFO")  # 设置日志级别为 INFO
    # 输出到控制台
    logger.add(sys.stdout, level="INFO")
    # 输出到文件
    logger.add("file.log", level="INFO")
    logger.info("This log will be printed to both console and file")
