package main

import (
	"flag"
	"fmt"
	"log"

	"github.com/atotto/clipboard"
)

func main() {
	log.SetPrefix("Error: ")
	log.SetFlags(0)

	fmt.Println("Creating password")

	var length = flag.Int("l", 8, "Length of password")
	var symbols = flag.Bool("s", true, "Pass have symbols")
	var numbers = flag.Bool("n", true, "Pass have numbers")

	flag.Parse()

	fmt.Printf("Length: %v, Numbers: %v, Symbols: %v \n", *length, *numbers, *symbols)

	password := createPassword(*length, *numbers, *symbols)
	fmt.Println("Password created: ", password)
	savePassword(password)
	error := clipboard.WriteAll(password)

	if error != nil {
		log.Fatal(error)
	} else {
		fmt.Println("Password copied to clipboard")
	}
}
