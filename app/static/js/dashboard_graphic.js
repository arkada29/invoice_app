var myChart = {}

function weeklyChartBarang(label, value){
const data = {
    labels : label,//year_product.filter(n=>n),
    datasets:[{
        label:'Barang label',
        data:value,
        backgroundColor: [
            'rgb(128,0,128)',
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(46,139,87)',
                        'rgb(255,153,51)',
                        'rgb(51,255,255)',
                        'rgb(255,51,255)',
                        'rgb(204,0,102)'
                        ],
                        borderColor:'blue',
                        borderWidth:0.5,
        // hoverBorderWidth:3,
        hoverBorderColor:'#000',
        hoverOffset: 1
    }]
};

const options = {
    responsive:true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: true,
            text: 'Sold Per Day',
            fontSize:'10',
            position:'top',
            font: {
                size: 10
            },
            color:'black'
        },
        // subtitle: {
        //     display: true,
        //     text: '(In Percent)',
        //     font: {
        //             size: 10
        //         },
        //     padding:10
        // },
        legend: {
            display:false,
            position:'bottom',
            labels: {
                // This more specific font property overrides the global property
                font: {
                    size: 8
                },
                boxWidth:10,
                color:'black'
            },
        },
        datalabels:{
            color:'black'
        }
    
    },
 

}
const config = {
    type:'bar',
    data:data,
    options:options,
    plugins: [ChartDataLabels]
}

const myChart = new Chart(
    document.getElementById('canvas-barang-data'),
    config
);

}

var myChart = {}

function weeklyChartUser(label, value){
const data = {
    labels : label,//year_product.filter(n=>n),
    datasets:[{
        label:'Barang label',
        data:value,
        backgroundColor: [
            'rgb(128,0,128)',
                        'rgb(255, 99, 132)',
                        'rgb(54, 162, 235)',
                        'rgb(46,139,87)',
                        'rgb(255,153,51)',
                        'rgb(51,255,255)',
                        'rgb(255,51,255)',
                        'rgb(204,0,102)'
                        ],
                        borderColor:'blue',
                        borderWidth:0.5,
        // hoverBorderWidth:3,
        hoverBorderColor:'#000',
        hoverOffset: 1
    }]
};

const options = {
    responsive:true,
    maintainAspectRatio: false,
    plugins: {
        title: {
            display: true,
            text: 'Joined User',
            fontSize:'10',
            position:'top',
            font: {
                size: 10
            },
            color:'black'
        },
        // subtitle: {
        //     display: true,
        //     text: '(In Percent)',
        //     font: {
        //             size: 10
        //         },
        //     padding:10
        // },
        legend: {
            display:false,
            position:'bottom',
            labels: {
                // This more specific font property overrides the global property
                font: {
                    size: 8
                },
                boxWidth:10,
                color:'black'
            },
        },
        datalabels:{
            color:'black'
        }
    
    },
 

}
const config = {
    type:'bar',
    data:data,
    options:options,
    plugins: [ChartDataLabels]
}

const myChart = new Chart(
    document.getElementById('canvas-user-data'),
    config
);

}

function weeklyChartVendor(label, value){
    const data = {
        labels : label,//year_product.filter(n=>n),
        datasets:[{
            label:'Barang label',
            data:value,
            backgroundColor: [
                'rgb(128,0,128)',
                            'rgb(255, 99, 132)',
                            'rgb(54, 162, 235)',
                            'rgb(46,139,87)',
                            'rgb(255,153,51)',
                            'rgb(51,255,255)',
                            'rgb(255,51,255)',
                            'rgb(204,0,102)'
                            ],
                            borderColor:'blue',
                            borderWidth:0.5,
            // hoverBorderWidth:3,
            hoverBorderColor:'#000',
            hoverOffset: 1
        }]
    };
    
    const options = {
        responsive:true,
        maintainAspectRatio: false,
        plugins: {
            title: {
                display: true,
                text: 'Sold Per Day',
                fontSize:'10',
                position:'top',
                font: {
                    size: 10
                },
                color:'black'
            },
            // subtitle: {
            //     display: true,
            //     text: '(In Percent)',
            //     font: {
            //             size: 10
            //         },
            //     padding:10
            // },
            legend: {
                display:false,
                position:'bottom',
                labels: {
                    // This more specific font property overrides the global property
                    font: {
                        size: 8
                    },
                    boxWidth:10,
                    color:'black'
                },
            },
            datalabels:{
                color:'black'
            }
        
        },
     
    
    }
    const config = {
        type:'bar',
        data:data,
        options:options,
        plugins: [ChartDataLabels]
    }
    
    const myChart = new Chart(
        document.getElementById('canvas-vendor-data'),
        config
    );
    
    }

    function weeklyChartPenjualan(label, value){
        const data = {
            labels : label,//year_product.filter(n=>n),
            datasets:[{
                label:'Barang label',
                data:value,
                backgroundColor: [
                    'rgb(128,0,128)',
                                'rgb(255, 99, 132)',
                                'rgb(54, 162, 235)',
                                'rgb(46,139,87)',
                                'rgb(255,153,51)',
                                'rgb(51,255,255)',
                                'rgb(255,51,255)',
                                'rgb(204,0,102)'
                                ],
                                borderColor:'blue',
                                borderWidth:0.5,
                // hoverBorderWidth:3,
                hoverBorderColor:'#000',
                hoverOffset: 1
            }]
        };
        
        const options = {
            responsive:true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: 'Sold Per Day',
                    fontSize:'10',
                    position:'top',
                    font: {
                        size: 10
                    },
                    color:'black'
                },
                // subtitle: {
                //     display: true,
                //     text: '(In Percent)',
                //     font: {
                //             size: 10
                //         },
                //     padding:10
                // },
                legend: {
                    display:false,
                    position:'bottom',
                    labels: {
                        // This more specific font property overrides the global property
                        font: {
                            size: 8
                        },
                        boxWidth:10,
                        color:'black'
                    },
                },
                datalabels:{
                    color:'black'
                }
            
            },
         
        
        }
        const config = {
            type:'bar',
            data:data,
            options:options,
            plugins: [ChartDataLabels]
        }
        
        const myChart = new Chart(
            document.getElementById('canvas-penjualan-data'),
            config
        );
        
        }

