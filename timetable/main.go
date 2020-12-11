package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/url"
	"os"
	"runtime"
	"strings"
)
// 不完整，主要接口分析完，填充对应 session即可
func handleErr(err error,layer int){
	if err!=nil{
		_, file, line, ok := runtime.Caller(layer)
		fmt.Printf("err in file:%s,  line: %d,  can recover = %#v  err:%s\n",file,line,ok,err)
		os.Exit(0)
	}
}
func initData(){
	resp,err := http.Post("https://app.upc.edu.cn/wap/setting/info","",nil)
	handleErr(err,2)
	defer resp.Body.Close()
	all, err := ioutil.ReadAll(resp.Body)
	fmt.Println(string(all))

	fmt.Printf("协议头:%s\n",resp.Header)
}
func Login(user,passwd string){
	forms := url.Values{}
	forms.Add("username",user)
	forms.Add("password",passwd)
	resp,err := http.PostForm("https://app.upc.edu.cn/uc/wap/login/check",forms)
	handleErr(err,2)
	defer resp.Body.Close()
	fmt.Printf("Header : %#v\n",resp.Header)
	all, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(all))
	//{"e":10011,"m":"账号或密码错误","d":{}}  {"e":0,"m":"操作成功","d":{}}
	if bytes.Index(all,[]byte("成功"))==-1{
		// 登录失败
		fmt.Println(string(all))
	}
}
func getIndex(){
	client := &http.Client{}
	req,err := http.NewRequest("GET","https://app.upc.edu.cn/timetable/wap/default/get-index",nil)
	handleErr(err,2)


	req.AddCookie(&http.Cookie{Name:"eai-sess",Value: "o47fkahkt2ps1m",HttpOnly: true})
	req.AddCookie(&http.Cookie{Name:"UUkey",Value: "9cce1ff7ee6",HttpOnly: true})

	resp, err := client.Do(req)
	handleErr(err,2)
	defer resp.Body.Close()
	all, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(string(all))
	/*{"e":0,"m":"操作成功","d":{"params":{"year":"2020-2021","term":"1","startday":"2020-09-06","countweek":"19","id":"13","week":3},"termInfo":[{"year":"2018-2019","term":"1","startday":"2
	//018-09-09","countweek":"18","id":"7"},{"year":"2018-2019","term":"2","startday":"2019-02-24","countweek":"18","id":"8"},{"year":"2018-2019","term":"3","startday":"2019-06-30","countwee
	//k":"4","id":"9"},{"year":"2019-2020","term":"1","startday":"2019-09-08","countweek":"18","id":"10"},{"year":"2019-2020","term":"2","startday":"2020-02-16","countweek":"18","id":"11"},{
	//"year":"2019-2020","term":"3","startday":"2020-06-21","countweek":"4","id":"12"},{"year":"2020-2021","term":"1","startday":"2020-09-06","countweek":"19","id":"13"},{"year":"2020-2021",
	//"term":"2","startday":"2021-02-28","countweek":"18","id":"14"},{"year":"2020-2021","term":"3","startday":"2021-07-04","countweek":"3","id":"15"}],"weekday":"3","weekdays":["2020-09-20"
	//,"2020-09-21","2020-09-22","2020-09-23","2020-09-24","2020-09-25","2020-09-26"]}}*/
}
func getData(){
	c := &http.Client{}
	form := "year=2020-2021&term=1&week=5&type=2"
	req,_ := http.NewRequest("POST","https://app.upc.edu.cn/timetable/wap/default/get-datatmp",strings.NewReader(form))
	
	req.AddCookie(&http.Cookie{Name:"eai-sess",Value: "9lmqeuh7",HttpOnly: true})
	req.AddCookie(&http.Cookie{Name:"UUkey",Value: "14a86",HttpOnly: true})

	req.Header.Add("Content-Type","application/x-www-form-urlencoded") //此协议头必须加


	resp, err := c.Do(req)
	handleErr(err,2)
	defer resp.Body.Close()
	all, _ := ioutil.ReadAll(resp.Body)
	fmt.Println(len(all))
	fmt.Println(string(all))

}
func main() {
	//initData() 不必要

	//getIndex()

	//Set-Cookie:[eai-sess=05
	//hsgqb5dk4; expires=Fri, 23-Oct-2020 11:47:21 GMT; Max-Age=2592000; path=/; HttpOnly UUkey=; e
	/*
	https://app.upc.edu.cn/wap/setting/info	 POST	获得2cookie
	eai-sess=nhtqnnhm4; expires=Fri, 23-Oct-2020 11:28:33 GMT; Max-Age=2592000; path=/; HttpOnly


	https://app.upc.edu.cn/uc/wap/login/check		POST
	Content-Type: application/x-www-form-urlencoded; charset=UTF-8
	Cookie
		eai-sess=1h8901; UUkey=08b
		formData:username=1019.

	getIndex :
	{"GET":{"scheme":"https","host":"app.upc.edu.cn","filename":"/timetable/wap/default/get-index","remote":{"地址":"211.87.178.171:443"}}}

	getData:
	POST
		https://app.upc.edu.cn/timetable/wap/default/get-datatmp

	*/
	Login(用户名,密码)
	getData()
}
