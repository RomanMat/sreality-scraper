# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import os


class LuxonisScraperPipeline:
    def __init__(self):
        ## Connection Details
        hostname = "db"
        username = os.environ.get("POSTGRES_USER")
        password = os.environ.get("POSTGRES_PASSWORD")  # your password
        database = os.environ.get("POSTGRES_NAME")

        ## Create/Connect to database
        self.connection = psycopg2.connect(
            host=hostname,
            user=username,
            password=password,
            dbname=database,
            port="5432",
        )

        ## Create cursor, used to execute commands
        self.cur = self.connection.cursor()

        ## Create quotes table if none exists
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS appartments (
                appartment_id SERIAL PRIMARY KEY,
                title varchar NOT NULL,
                img_url varchar
            );
        """
        )

    def process_item(self, item, spider):
        ## Check to see if text is already in database
        self.cur.execute(
            "select * from appartments where title = %s AND img_url = %s",
            (item["title"], item["img_url"]),
        )
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item["title"])

        ## If name isn't in the DB, insert data
        else:
            ## Define insert statement
            self.cur.execute(
                "insert into appartments(title,img_url) values(%s,%s)",
                (item["title"], item["img_url"]),
            )
            ## Execute insert of data into database
            self.connection.commit()
        return item

    def close_spider(self, spider):
        ## Close cursor & connection to database
        self.cur.close()
        self.connection.close()
