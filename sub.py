from subprocess import Popen, PIPE
import requests
import webbrowser


def execute(cmd):
    args = cmd.split()
    pro = Popen(args, stdout= PIPE, stderr= PIPE)
    #print(pro)
    out, err = pro.communicate()
    #print(out)
    error_string = err.decode(encoding = 'UTF-8').strip().split('\r\n')[-1]
    return error_string


def make_request(error):
    resp= requests.get("https://api.stackexchange.com/"+"/2.2/search?order=desc&sort=votes&tagged=python&intitle={}&site=stackoverflow".format(error))
    return resp.json()


def get_links(json_item):
    links_list = []
    count = 0
    for item in json_item["items"]:
        if item["is_answered"]:
            links_list.append(item["link"])
            count = count + 1
        if count == 2 :
            break
    for link in links_list:
        webbrowser.open(link)



def main():
    path = input("Enter file name or path: ")
    error_string = execute(path)
    print(error_string)
    if error_string:
        error_type = error_string.split(':')[0]
        error_message = error_string.split(':')[-2].strip()
        # print(error_type)
        # print(error_message)

        json1 = make_request(error_type)
        json2 = make_request(error_message)
        json3 = make_request(error_string)
        get_links(json1)
        get_links(json2)
        get_links(json3)

    else:
        print("Code Execution Successful")


if __name__ == '__main__':
    main()
