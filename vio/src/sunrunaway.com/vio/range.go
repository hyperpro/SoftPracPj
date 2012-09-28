package vio

import (
	"strconv"
	"strings"
)

func parseRange1(rg string, fsize int64) (from int64, to int64, ok bool) {

	pos := strings.Index(rg, "-")
	if pos == -1 {
		return
	}

	from1 := strings.Trim(rg[:pos], " \t")
	to1 := strings.Trim(rg[pos+1:], " \t")

	var err error
	if from1 != "" {
		from, err = strconv.ParseInt(from1, 10, 64)
		if err != nil {
			return
		}
		if to1 != "" { // start-end
			to, err = strconv.ParseInt(to1, 10, 64)
			if err != nil {
				return
			}
			to++
		} else { // val-
			to = fsize
		}
	} else { // -val
		if to1 == "" {
			return
		}
		from, err = strconv.ParseInt(to1, 10, 64)
		if err != nil {
			return
		}
		to = fsize
		from = to - from
	}

	ok = from < to && to <= fsize
	return
}

func ParseOneRange(rg2 string, fsize int64) (from int64, to int64, ok bool) {
	pos := strings.Index(rg2, "=")
	if pos == -1 {
		return
	}
	return parseRange1(rg2[pos+1:], fsize)
}
