var jerryLeeWatchlistStore = Ext.create('Grdt.watchlist.Store',{
    storeId: 'jerryLeeWatchlistStore',
    listeners : {
        load: function(thiz, records, successful, operation, eOpts ) {
          var store = thiz;
          var comboBox = Ext.getCmp('jerryLeeWatchlistComboBox');;
          // On screen load default watchlist combobox to DEFAULT watchlist
          if(successful) {
            if(!comboBox.getValue()) {
              var tickerIndex = store.find('name','DEFAULT');
              comboBox.setValue(records[tickerIndex]);
            }
          }
        }
    }
});


var jerryLeeWatchlistComboBox = Ext.create('Grdt.watchlist.ComboBox', {
    id: 'jerryLeeWatchlistComboBox',
    store: jerryLeeWatchlistStore,
});

var jerryLeeDatePicker = {
            xtype: 'datefield',
            fieldLabel: 'Date',
            name:'searchDate',
            labelAlign:'right',
            value: new Date(),
        };
        
var jerryLeeTimeComboBox = Ext.create('Grdt.time.ComboBox', {
    id: 'jerryLeeTimeComboBox',
});
        
var jerryLeeSearchButton = Ext.create('Ext.Button', {
    text: 'GO',
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
        {  
            xtype: 'tbspacer', width:15,
        },
        jerryLeeSearchButton,
    ],
});

Ext.define('JerryLeeModel', {
     extend: 'Ext.data.Model',
     fields: [
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
            //watchlist: Ext.getCmp('jerryLeeWatchlistComboBox').getValue(),
            //hour: Ext.getCmp('jerryLeeTimeComboBox').getValue(),
            //searchDate:,
        },
     },
     autoLoad: false,
     listeners: {
         beforeload: function(store, operation, eOpts) {
            var formData = Ext.getCmp('jerryLeeSearchBar').getForm().getValues();
            Ext.apply(operation._proxy.extraParams, formData);
         }
     }
});

var jerryLeeGrid = Ext.create('Ext.grid.Panel', {
    store:Ext.data.StoreManager.lookup('jerryLeeStore'), 
    width: '100%',
    height: '100%',
    columns: [
        //{ text: 'optionType', dataIndex: 'putOptionType', flex:0.5 },
        { text: 'Puts', dataIndex: 'putNasdaqName' , flex:0.6},
        { text: 'Strike', dataIndex: 'putStrike' , flex:0.5}, // already displayed by callStrike as they are the same
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