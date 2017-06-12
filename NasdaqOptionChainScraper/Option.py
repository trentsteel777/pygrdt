class Option(models.Model):
    
    CALL = 'CALL'
    PUT = 'PUT'
    
    OPTION_TYPES = (
        ( CALL, 'CALL' ),
        ( PUT, 'PUT' ),
    )
    
    optionType = models.CharField(
        max_length=4,
        choices=OPTION_TYPES,
        primary_key=True,
    )
    timestamp = models.DateTimeField(
        primary_key=True,
    )
    
    optionChain = models.ForeignKey(OptionChain, on_delete=models.CASCADE)
     
    nasdaqName = models.CharField(max_length=30)
    contractName = models.CharField(max_length=30)
    last = models.DecimalField(max_digits=8, decimal_places=2)
    change = models.DecimalField(max_digits=4, decimal_places=2)
    bid = models.DecimalField(max_digits=8, decimal_places=2)
    ask = models.DecimalField(max_digits=8, decimal_places=2)
    volume = models.IntegerField()
    openInterest = models.IntegerField()
    ticker = models.CharField(max_length=5)
    strike = models.DecimalField(max_digits=12, decimal_places=2)

        
    def getIds(self):
        return '[ ' + self.ticker + ' ' + self.type + ' ' + self.nasdaqName + ' ]'

    def getOptionType(self):
        return ''

    def getExpirationType:
        return ''
