package store

import (
	"io"
	"os"
	"os/exec"
	"path"
	"errors"
)

var (
	EThumb = errors.New("Get thumb failed.")
)

type ReadSeekCloser interface {
	io.ReadSeeker
	io.Closer
}

type Store struct {
	root string
}

func NewStore(root string) *Store {
	return &Store{root}
}

// =============================================================================

func (s *Store) Check(key string) bool {
	filename := path.Clean(s.root + "/" + key)
	_, err := os.Stat(filename)
	if err != nil {
		return false
	}
	return true
}

// -----------------------------------------------------------------------------

func (s *Store) Get(key string) (r ReadSeekCloser, length int64, err error) {
	filename := path.Clean(s.root + "/" + key)

	f, err := os.Open(filename)
	if err != nil {
		return
	}

	fi, err := os.Stat(filename)
	if err != nil {
		return
	}
	fsize := fi.Size()

	return f, fsize, nil
}

// -----------------------------------------------------------------------------

type fileRemover struct {
	f *os.File
}

func (s *fileRemover) Read(b []byte) (n int, err error) {
	return s.f.Read(b)
}

func (s *fileRemover) Seek(offset int64, whence int) (ret int64, err error) {
	return s.f.Seek(offset, whence)
}

func (s *fileRemover) Close() error {
	s.f.Close()
	os.Remove(s.f.Name())
	return nil
}

const coverImg = "/tmp/cover.jpg"

func (s *Store) GetThumb(key string, mode string) (r ReadSeekCloser, length int64, err error) {

	filename := path.Clean(s.root + "/" + key)

	var cmd *exec.Cmd
	switch mode {
	case "0":
		cmd = exec.Command("ffmpeg", "-ss", "00:00:02", "-i", filename, coverImg, "-r", "1", "-vframes", "1", "-an", "-f", "mjpeg")
	case "1":
		cmd = exec.Command("ffmpeg", "-ss", "00:00:02", "-i", filename, "-s", "200x150", coverImg, "-r", "1", "-vframes", "1", "-an", "-f", "mjpeg")
	}

	if cmd == nil {
		err = EThumb
		return
	}
	cmd.Run()

	f, err := os.Open(coverImg)
	if err != nil {
		return
	}

	fi, err := os.Stat(coverImg)
	if err != nil {
		f.Close()
		os.Remove(f.Name())
		return
	}
	fsize := fi.Size()

	return &fileRemover{f}, fsize, nil
}

// -----------------------------------------------------------------------------

func (s *Store) Put(key string, r io.Reader, length int64) (err error) {
	filename := path.Clean(s.root + "/" + key)

	defer func() {
		if err != nil {
			os.Remove(filename)
		}
	}()

	f, err := os.Create(filename)
	if err != nil {
		return
	}
	defer f.Close()

	n, err := io.CopyN(f, r, length)
	if err != nil || n != length {
		if n != length {
			err = io.ErrShortWrite
		}
		return
	}

	return
}

// -----------------------------------------------------------------------------

func (s *Store) Delete(key string) (err error) {
	filename := path.Clean(s.root + "/" + key)
	err = os.Remove(filename)
	return
}
