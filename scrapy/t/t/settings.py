# Scrapy settings for imax project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 't'

SPIDER_MODULES = ['t.spiders']
NEWSPIDER_MODULE = 't.spiders'

ITEM_PIPELINES = {
    't.pipelines.JsonWriterPipeline': 800,
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'imax (+http://www.yourdomain.com)'
