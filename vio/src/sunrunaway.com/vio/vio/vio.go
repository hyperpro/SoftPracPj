package main

import (
	"log"
	"os"
	"flag"
	"io/ioutil"
	"encoding/json"
	"sunrunaway.com/store"
	"sunrunaway.com/vio"
)

const (
	default_conf = "vio.conf"
)

type Message struct {
	BindHost      string `json:"bind_host"`
	Root          string `json:"data_root"`
	MyHost        string `json:"my_host"`
	UrlExpireTime int64 `json:"url_expire_time"`
}

func main() {

	confName := flag.String("f", default_conf, "the config file")
	flag.Parse()

	var cfg Message
	data, err := ioutil.ReadFile(*confName)
	if err != nil {
		log.Fatal(err)
	}
	err = json.Unmarshal(data, &cfg)
	if err != nil {
		log.Fatal(err)
	}


	os.Mkdir(cfg.Root, 0755)
	stg := store.NewStore(cfg.Root)
	service := vio.New(stg, cfg.MyHost, cfg.UrlExpireTime)
	err = service.Run(cfg.BindHost)
	log.Fatal(err)
}
