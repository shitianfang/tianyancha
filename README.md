# tianyancha

涉及到API调用和自动化，通过获取tycid和auth_token进行认证，未公开API的部分用自动化爬虫完成，有API使用正常request不能获取到，需要用浏览器模拟打开获取数据，暂时未知原因，难度在3星左右，
相对于法律文书网（5星）和 bilibiliAPI（2星），
模块分为parser，spider，config三部分，parser负责页面解析逻辑以及API数据获取，spider负责爬虫整体逻辑，config负责Headers以及填写爬虫相关配置，
数据流向为spider -> parser（config -> self）-> spider，cookies目录负责保存登录后的cookies，如果cookie过期需要删除文件重新进行登录
