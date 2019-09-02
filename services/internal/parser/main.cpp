// g++ main.cpp -lmysqlclient -lcurl

#include <iostream>
#include <vector>
#include <string>

#include <curl/curl.h>
#include <myhtml/api.h>
#include <mysql/mysql.h>
//#include <cpr/cpr.h>

#include "../../../lib/cpp/database.cpp"

#define DB_SERVER "localhost"
#define DB_USER "tester"
#define DB_PASSWORD "tester123"
#define DB_DATABASE "crawline"

#define CURL_VERSION "curl/7.58.0"

using namespace std;

struct domain
{
	int id;
	string name;
};

vector<domain> get_domains(Database *db, unsigned int limit, unsigned int offset)
{
	string query = "SELECT * FROM valid_domains LIMIT " + to_string(limit) + " OFFSET " + to_string(offset);

	vector<domain> domains = {};
	vector<MYSQL_ROW> rows = db->fetch_by_query(query);

	for(MYSQL_ROW row : rows)
	{
		domain d = {.id = stoi(row[0]), .name = row[1]};
		domains.push_back(d);
	}

	return domains;
}

class Scraper
{
	public:
		Scraper(Database *db):
		_db{db}{}

		struct response;

	private:
		Database *_db;
		// Add curl helper here
};

int main()
{
	Database db(DB_SERVER, DB_USER, DB_PASSWORD, DB_DATABASE);

	if(!db.connected())
	{
		cout << "Database connection error. Latest MySQL log: " << db.last_log() << endl;
		return 1;
	}

	vector<domain> domains = get_domains(&db, 1, 0);
	auto size = domains.size();

	if (size > 0)
	{
		Scraper scraper(&db);

		// Check if pointer can go here.
		for (domain d : domains)
		{
			cout << "Parsing domain: " << d.name << endl;

			string url = "https://" + d.name;
			url = "http://aikido-zadar.hr";
		}
	}
	else
	{
		cout << "No valid domains available. Latest MySQL log: " << db.last_log() << endl;
	}

  return 0;
}
