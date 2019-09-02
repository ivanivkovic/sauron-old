#include <string>
#include <vector>
#include <mysql/mysql.h>

using namespace std;

class Database
{
	public:
		Database(string server, string user, string password, string database);
		~Database();

		string last_log();
		vector<MYSQL_ROW> fetch_by_query(string query);
		bool connected();

	private:
		MYSQL *_conn;
		string _last_log;
		bool _connected = false;
};

Database::Database(string server, string user, string password, string database)
{
	_conn = mysql_init(NULL);

	if(_conn)
	{
		if(!mysql_real_connect(_conn, server.c_str(), user.c_str(), password.c_str(), database.c_str(), 0, NULL, 0))
		{
			_last_log = mysql_error(_conn);
		}
		else
		{
			_connected = true;
		}
	}
	else
	{
		_last_log = "MySQL initialization failed! Is your MySQL connector correctly installed?";
	}
}

Database::~Database()
{
	mysql_close(_conn);
  delete _conn;
}

string Database::last_log()
{
	return _last_log;
}

bool Database::connected()
{
	return _connected;
}

vector<MYSQL_ROW> Database::fetch_by_query(string query)
{
	MYSQL_RES *result;
	MYSQL_ROW row;

	vector<MYSQL_ROW> rows = {};

	if(mysql_query(_conn, query.c_str()))
	{
		_last_log = mysql_error(_conn);
	}
	else
	{
    result = mysql_store_result(_conn);

		while ((row = mysql_fetch_row(result)) != NULL)
    {
			rows.push_back(row);
		}

		mysql_free_result(result);
	}

	return rows;
}
