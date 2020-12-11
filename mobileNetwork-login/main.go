package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"strings"
)
// only mobile && AP:UPC
func login(uname, passwd string) bool {
	login := `userId=%s&password=%s`
	str := `&service=cmcc&queryString=wlanuserip%253D180.201.131.175%2526wlanacname%253D%2526nasip%253D172.22.242.21%2526wlanparameter%253De4-54-e8-06-c3-7c%2526url%253Dhttp%253A%252F%252Fwww.upc.edu.cn%252F%2526userlocation%253Dethtrunk%252F62%253A1154.0&operatorPwd=&operatorUserId=&validcode=&passwordEncrypt=false`
	userReader := strings.NewReader(fmt.Sprintf(login, uname, passwd) + str)
	req, err := http.NewRequest("POST", "http://lan.upc.edu.cn/eportal/InterFace.do?method=login", userReader)
	req.Header.Add("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8")
	if err != nil {
		fmt.Printf("new req err %s\n", err.Error())
		return false
	}
	client := &http.Client{}
	resp, _ := client.Do(req)
	defer resp.Body.Close()
	all, _ := ioutil.ReadAll(resp.Body)
	if bytes.Index(all, []byte(`"result":"success"`)) > 0 {
		return true
	}
	return false
}
func main() {
	login(用户名,密码)
}
