import middleware
import bot
import readConfig

if __name__ == '__main__':
    conf = readConfig.ReadConfig('config.ini')

    # com = middleware.Communication(conf.localHost, conf.host, conf.port)

    bot = bot.Bot(conf.localHost, conf.host, conf.port)

    bot.getAIInfo(conf.minSpeed, conf.maxSpeed, conf.moveDistance, conf.startAngle, conf.endAngle, conf.targetPoint, conf.moveProbability, conf.scoutProbability, conf.attackProbability)
    
    bot.run(conf.frequency)