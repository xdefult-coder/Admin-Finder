package main

import (
    "fmt"
    "net/http"
    "os"
    "bufio"
    "sync"
)

var wg sync.WaitGroup
var foundCount int
var mutex = &sync.Mutex{}

func scanURL(base, path string) {
    defer wg.Done()
    url := base + "/" + path
    resp, err := http.Get(url)
    if err == nil {
        if resp.StatusCode == 200 || resp.StatusCode == 301 || resp.StatusCode == 302 || resp.StatusCode == 403 {
            mutex.Lock()
            foundCount++
            fmt.Printf("[FOUND] %s -> %d\n", url, resp.StatusCode)
            mutex.Unlock()
        }
        resp.Body.Close()
    }
}

func main() {
    if len(os.Args) < 2 {
        fmt.Println("Usage: go run def4ult_admin_finder.go <target-url>")
        return
    }
    baseUrl := os.Args[1]

    file, err := os.Open("../wordlists/admin_paths.txt")
    if err != nil {
        fmt.Println("Error reading wordlist:", err)
        return
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        wg.Add(1)
        go scanURL(baseUrl, scanner.Text())
    }

    wg.Wait()
    fmt.Printf("[+] Scan Complete. Total Found: %d\n", foundCount)
}
