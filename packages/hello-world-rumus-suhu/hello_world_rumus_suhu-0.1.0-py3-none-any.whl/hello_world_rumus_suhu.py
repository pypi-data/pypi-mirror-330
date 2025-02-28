class helloWorld:
    def __init__(self):
        print("Hello World")
    def sayHello(nama):
        print(f"Hello {nama}!")
    def usia(tahun_sekarang, tahun_lahir):
        print(f"Usia anda sekarang {tahun_sekarang - tahun_lahir} tahun")
    
class rumusSuhu:
    def __init__(self):
        print("Rumus Suhu")
    def celciusToFahrenheit(celcius):  
        print(f"{celcius} derajat celcius adalah {celcius * 9/5 + 32} derajat fahrenheit")
    def fahrenheitToCelcius(fahrenheit):
        print(f"{fahrenheit} derajat fahrenheit adalah {(fahrenheit - 32) * 5/9} derajat celcius")
    def celciusToKelvin(celcius):
        print(f"{celcius} derajat celcius adalah {celcius + 273.15} derajat kelvin")
    def kelvinToCelcius(kelvin):
        print(f"{kelvin} derajat kelvin adalah {kelvin - 273.15} derajat celcius")
    def fahrenheitToKelvin(fahrenheit):
        print(f"{fahrenheit} derajat fahrenheit adalah {(fahrenheit - 32) * 5/9 + 273.15} derajat kelvin")
    def kelvinToFahrenheit(kelvin):
        print(f"{kelvin} derajat kelvin adalah {(kelvin - 273.15) * 9/5 + 32} derajat fahrenheit")