all:
	go install ./...

install: all
	@echo

test:
	go test ./...

clean:
	rm -r bin; rm -r pkg

run:	all
	./bin/vio -f ./src/sunrunaway.com/vio/vio/vio.conf
