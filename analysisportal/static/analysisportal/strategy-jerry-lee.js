var NO_DATA = 'NO_DATA';
var applyJerryLeeSearchBarValuesToParams = function(store, operation, eOpts) {
    var formData = Ext.getCmp('jerryLeeSearchBar').getForm().getValues();
    Ext.apply(operation._proxy.extraParams, formData);
};

var resetOptionExpiryStoreAndSearchButton = function(){
    Ext.data.StoreManager.lookup('jerryLeeOptionExpiryStore').removeAll();
    Ext.getCmp('jerryLeeSearchButton').setDisabled(true);
    Ext.getCmp('jerryLeeOptionExpiryComboBox').clearValue();
}; 

var jerryLeeOptionExpiryStore = Ext.create('Grdt.optionexpiry.Store',{
    storeId: 'jerryLeeOptionExpiryStore',
    listeners: {
    
        beforeload: applyJerryLeeSearchBarValuesToParams, 
         
        load: function(thiz, records, successful, operation, eOpts ) {
          var store = thiz;
          var comboBox = Ext.getCmp('jerryLeeOptionExpiryComboBox');
          // On screen load default watchlist combobox to DEFAULT watchlist
          if(successful) {
            var searchButton = Ext.getCmp('jerryLeeSearchButton');
            if(!records.length) {
              comboBox.setRawValue(NO_DATA);
              searchButton.setDisabled(true);
            }
            else {
              // second record should be month ahead, which is normally what we are searching for 
              // with Jerry Lee strategy
              if(records.length >= 3) {
                comboBox.setRawValue(records[2].data.expiry);
              }
              searchButton.setDisabled(false);
            }
          }
        }
    }
});


var jl_searchBarChanges = function() {
    var oldWatchlist;
    var oldDate;
    var oldHour;
    
    return {
      isChanged: function() {
        var newWatchlist = Ext.getCmp('jerryLeeWatchlistComboBox').getValue();
        var newDate = Ext.getCmp('jerryLeeDatePicker').getValue();
        var newHour = Ext.getCmp('jerryLeeTimeComboBox').getValue(); 
        
        return  (
            (oldWatchlist !== newWatchlist) ||
            (oldDate !== newDate) ||
            (oldHour !== newHour) )
            
      },
      update: function() {
        oldWatchlist = Ext.getCmp('jerryLeeWatchlistComboBox').getValue();
        oldDate = Ext.getCmp('jerryLeeDatePicker').getValue();
        oldHour = Ext.getCmp('jerryLeeTimeComboBox').getValue(); 
      }
    };
    
}();

var jerryLeeOptionExpiryComboBox = Ext.create('Grdt.optionexpiry.ComboBox', {
    id: 'jerryLeeOptionExpiryComboBox',
    store: jerryLeeOptionExpiryStore,
    editable: false,
    lastQuery: '',
    listeners: {
        // delete the previous query in the beforequery event or set
        // combo.lastQuery = null (this will reload the store the next time it expands)
        beforequery: function(qe){
            if(jl_searchBarChanges.isChanged()) {
              delete qe.combo.lastQuery;
              jl_searchBarChanges.update();
            }
        }
    }
});

var jerryLeeWatchlistStore = Ext.create('Grdt.watchlist.Store',{
    storeId: 'jerryLeeWatchlistStore',
    listeners : {
        load: function(thiz, records, successful, operation, eOpts ) {
          var store = thiz;
          var comboBox = Ext.getCmp('jerryLeeWatchlistComboBox');
          // On screen load default watchlist combobox to DEFAULT watchlist
          if(successful) {
            if(!comboBox.getValue()) {
              var tickerIndex = store.find('name','DEFAULT');
              comboBox.setValue(records[tickerIndex]);
            }
          }
        },
        change: resetOptionExpiryStoreAndSearchButton,
    }
});


var jerryLeeWatchlistComboBox = Ext.create('Grdt.watchlist.ComboBox', {
    id: 'jerryLeeWatchlistComboBox',
    store: jerryLeeWatchlistStore,
});

var jerryLeeDatePicker = {
            xtype: 'datefield',
            id :'jerryLeeDatePicker',
            fieldLabel: 'Date',
            name:'searchDate',
            labelAlign:'right',
            value: new Date(),
            listeners: {
                change: resetOptionExpiryStoreAndSearchButton,
            }
        };
        
var jerryLeeTimeComboBox = Ext.create('Grdt.time.ComboBox', {
    id: 'jerryLeeTimeComboBox',
    listeners: {
        change: resetOptionExpiryStoreAndSearchButton,
    }
});
        
var jerryLeeSearchButton = Ext.create('Ext.Button', {
    id :'jerryLeeSearchButton',
    text: 'GO',
    disabled: true,
    autoLoad: false,
    handler: function() {
        Ext.data.StoreManager.lookup('jerryLeeStore').load();
    }
});

var jerryLeeSearchBar = Ext.create('Ext.form.Panel', {
    id: 'jerryLeeSearchBar',
    bodyPadding: 5, // Don't want content to crunch against the borders
    width: '100%',
    height: 40,
    url: PORTAL_URL,
    baseParams: {
        action: 'strategyJerryLee'
    },
    layout: 'hbox',
    //title: 'Search ',
    items: [
        jerryLeeWatchlistComboBox,
        jerryLeeDatePicker,
        jerryLeeTimeComboBox,
        jerryLeeOptionExpiryComboBox,
        {  
            xtype: 'tbspacer', width:15,
        },
        jerryLeeSearchButton,
    ],
});

Ext.define('JerryLeeModel', {
     extend: 'Ext.data.Model',
     fields: [
     
        {name: 'ticker',         type: 'string'},
        {name: 'marginOfSafety',   type: 'number'},
        {name: 'return',   type: 'number'},
        {name: 'margin', type: 'number'},
        {name: 'exposure',         type: 'number'},
        {name: 'earningsDate',         type: 'date'},
        
        {name: 'putOptionType',   type: 'string'},
        {name: 'putNasdaqName',   type: 'string'},
        {name: 'putContractName', type: 'string'},
        {name: 'putLast',         type: 'number'},
        {name: 'putChange',       type: 'number'},
        {name: 'putBid',          type: 'number'},
        {name: 'putAsk',          type: 'number'},
        {name: 'putVolume',       type: 'int'},
        {name: 'putOpenInterest', type: 'number'},
        {name: 'putStrike',       type: 'number'},
     ]
 });

 var jerryLeeStore = Ext.create('Ext.data.Store', {
    storeId: 'jerryLeeStore',
    model: 'JerryLeeModel',
    pageSize:GRID_PAGE_SIZE, // calls and puts get combined into one line per strike
     proxy: {
         type: 'ajax',
         url: PORTAL_URL,
         reader: {
             type: 'json',
             rootProperty: 'options',
             totalProperty: 'optionsTotal',
         },
         extraParams: {
            action: 'strategyJerryLee',
        },
     },
     autoLoad: false,
     listeners: {
         beforeload: applyJerryLeeSearchBarValuesToParams,
     }
});

var toDecimal = function(value) {
    return (value * 100).toFixed(2);
};

var jerryLeeGrid = Ext.create('Ext.grid.Panel', {
    store:Ext.data.StoreManager.lookup('jerryLeeStore'), 
    width: '100%',
    height: '100%',
    columns: [
        //{ text: 'optionType', dataIndex: 'putOptionType', flex:0.5 },
        
        { text: 'Ticker', dataIndex: 'ticker' , flex:0.5},
        { text: 'Puts', dataIndex: 'putNasdaqName' , flex:0.6},
        { text: 'Strike', dataIndex: 'putStrike' , flex:0.5}, // already displayed by callStrike as they are the same
        
        { text: 'MOS (%)', dataIndex: 'marginOfSafety', flex:0.6, renderer: toDecimal, 
        tooltip: new Ext.tip.ToolTip({
            target: this,
            html: 'Margin of Safety'
        })
        },
        { text: 'Return (%)', dataIndex: 'return' , flex:0.6, renderer: toDecimal, },
        { text: 'Margin ($)', dataIndex: 'margin' , flex:0.6},
        { text: 'Exposure', dataIndex: 'exposure' , flex:0.6},
        { text: 'Earnings', formatter:'date("Y-m-d")',dataIndex: 'earningsDate' , flex:0.6 },
        
        //{ text: 'contractName', dataIndex: 'putContractName', flex:0.5 },
        { text: 'Last', dataIndex: 'putLast' , flex:0.5},
        { text: 'Change', dataIndex: 'putChange' , flex:0.4},
        { text: 'Bid', dataIndex: 'putBid' , flex:0.5},
        { text: 'Ask', dataIndex: 'putAsk' , flex:0.5},
        { text: 'Volume', dataIndex: 'putVolume', flex:0.5 },
        { text: 'Open Interest', dataIndex: 'putOpenInterest' , flex:0.5},
        
        
    ],
    tbar:jerryLeeSearchBar,
    bbar:Ext.create('Ext.PagingToolbar', {
        store: jerryLeeStore,
        displayInfo: true,
        height:50,
        displayMsg: 'Displaying Puts {0} - {1} of {2}',
        emptyMsg: "No data to display"
    }),
});

var jerryLeePanel =  Ext.create('Ext.Panel', {
    title: 'Jerry Lee',
    id :'jerryLeePanel',
    height: '100px',
    width: '50px',
    layout :'fit',
    items: [
        jerryLeeGrid,
    ],
});