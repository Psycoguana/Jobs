class House:
    def __init__(self, link, address, city, status, property_year, date_on_market, price, square_feet, price_per_square_feet, schools_names, taxableLandValue, taxableImprovementValue, rollYear, taxesDue):
        self.link = link
        self.address = address
        self.city = city
        self.status = status
        self.property_year = property_year
        self.date_on_market = date_on_market
        self.price = price
        self.square_feet = square_feet
        self.price_per_square_feet = price_per_square_feet
        self.school_names = schools_names
        self.taxableLandValue = taxableLandValue
        self.taxableImprovementValue = taxableImprovementValue
        self.rollYear = rollYear
        self.taxesDue = taxesDue

    def __repr__(self):
        return self.link
