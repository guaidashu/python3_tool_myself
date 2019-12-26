# **Tool-yy, designed by yy**

## Installing and Getting started

1. Install

    The easiest way to install.
    
        pip install tool-yy
  
    Or you can clone source code from github.
  
        git clone git@github.com:guaidashu/python3_tool_myself.git

3. Start

    Example

  	    from tool_yy import Helper
  	    
  	    def create_helper():
  	        helper = Helper()
            helper.config.from_object('app.config.setting')
            return helper
  	    
  	    if __name__ == "__main__":
  	        helper = create_helper()
            db = helper.init_db("INSOMNIA_MUSIC_DATABASE_CONFIG")

    If you use it for the first time, you should create a file called "**app/config/setting.py**" in the directory called config which in the root path.
    
    And if you want to use the db. You should input these code in **app/config/setting.py**.
        
        INSOMNIA_MUSIC_DATABASE_CONFIG = {
            "MYSQL_DATABASE": "database",
            "MYSQL_USERNAME": "username",
            "MYSQL_PASSWORD": "password",
            "MYSQL_HOST": "localhost",
            "MYSQL_PORT": "3306"
        }


## Usage

None

## FAQ

None

## Running Tests

## Finally Thanks 

Thanks for your support.