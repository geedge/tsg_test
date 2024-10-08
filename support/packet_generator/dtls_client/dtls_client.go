package main

/*
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
*/
import "C"
import (
	"fmt"
	"net"
	"runtime"
	"unsafe"

	"github.com/pion/dtls/v2"
	"github.com/spf13/viper"
)

type Config struct {
	ServerIP   string
	ServerPort string
}

func main() {
	result := SimulateDtlsClient()
	fmt.Print("Test result:", result)
}

//export SimulateDtlsClient
func SimulateDtlsClient() *C.char {
	// certificate, err := tls.LoadX509KeyPair("d:/server.crt", "d:/server.key")
	// if err != nil {
	// 	log.Fatal(err)
	// }

	config := &dtls.Config{
		PSKIdentityHint: []byte("hint"),
		PSK:             pskCallback,
		CipherSuites:    []dtls.CipherSuiteID{dtls.TLS_PSK_WITH_AES_128_CCM_8},
		// Certificates:    []tls.Certificate{certificate},
		// ClientAuth: dtls.ClientAuthType(tls.RequireAndVerifyClientCert),
		ServerName: "abc.com",
	}

	var tempStr string

	viper.SetConfigName("config")
	viper.SetConfigType("toml")
	switch runtime.GOOS {
	case "linux":
		viper.AddConfigPath("/app/support/packet_generator/dtls_client")
	case "windows":
		viper.AddConfigPath("D:/Document/Project-TSG/Code/git/dtls_client")
	}
	if err := viper.ReadInConfig(); err != nil {
		fmt.Printf("Error reading config file, %s", err)
		tempStr = "Error reading config file"
		cTempStr := C.CString(tempStr)
		defer C.free(unsafe.Pointer(cTempStr))
		return cTempStr
	}
	serverIP := viper.GetString("server.ip")
	serverPort := viper.GetString("server.port")
	serverUrl := fmt.Sprintf("%s:%s", serverIP, serverPort)
	addr, err := net.ResolveUDPAddr("udp", serverUrl)
	if err != nil {
		fmt.Printf("Error resolving address: %v", err)
		tempStr = "Error resolving address"
		cTempStr := C.CString(tempStr)
		defer C.free(unsafe.Pointer(cTempStr))
		return cTempStr
	}
	conn, err := dtls.Dial("udp", addr, config)
	if err != nil {
		fmt.Printf("Failed to dial: %v", err)
		tempStr = "Failed to dial"
		cTempStr := C.CString(tempStr)
		defer C.free(unsafe.Pointer(cTempStr))
		return cTempStr
	}
	defer conn.Close()

	message := "Hello, DTLS!"
	_, err = conn.Write([]byte(message))
	if err != nil {
		fmt.Printf("Failed to write: %v", err)
		tempStr = "Failed to write"
		cTempStr := C.CString(tempStr)
		defer C.free(unsafe.Pointer(cTempStr))
		return cTempStr
	}

	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		fmt.Printf("Failed to read: %v", err)
		tempStr = "Failed to read"
		cTempStr := C.CString(tempStr)
		defer C.free(unsafe.Pointer(cTempStr))
		return cTempStr
	}

	fmt.Printf("Received from server: %s\n", buffer[:n])
	bufStr := "Received from server: " + string(buffer[:n])
	cStr := C.CString(bufStr)
	defer C.free(unsafe.Pointer(cStr))
	return cStr
}

func pskCallback(hint []byte) ([]byte, error) {
	return []byte("secret"), nil
}
