const getOptionProducts = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/get_products/');
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(error);
    }
}

const getOptionFavorites = async () => {
    try {
        const response = await fetch('http://127.0.0.1:8000/get_favorite/');
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(error);
    }
}

const getOptionSellers = async () => {
    try{
        const response = await fetch('http://127.0.0.1:8000/get_sellers/');
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(error);
    }
}

const getOptionCart = async () => {
    try{
        const response = await fetch('http://127.0.0.1:8000/get_products_cart/');
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(error);
    }
}

const initChart_products = async () => {
    const myChart = echarts.init(document.getElementById('chart1'));
    myChart.setOption(await getOptionProducts());
    myChart.resize();
}

const initChart_favorites = async () => {
    const myChart = echarts.init(document.getElementById('chart2'));
    myChart.setOption(await getOptionFavorites());
    myChart.resize();
}

const initChart_sellers = async () => {
    const myChart = echarts.init(document.getElementById('chart3'));
    myChart.setOption(await getOptionSellers());
    myChart.resize();
}

const initChart_cart = async () => {
    const myChart = echarts.init(document.getElementById('chart4'));
    myChart.setOption(await getOptionCart());
    myChart.resize();
}

window.addEventListener('load', async () => {
    try {
        const [productsData, favoritesData, sellerData, cartData] = await Promise.all([
            getOptionProducts(),
            getOptionFavorites(),
            getOptionSellers(),
            getOptionCart()
        ]);
        // Inicializa los gráficos después de que ambas promesas se hayan resuelto.
        initChart_products(productsData);
        initChart_favorites(favoritesData);
        initChart_sellers(sellerData);
        initChart_cart(cartData);
    } catch (error) {
        alert(error.message);
    }
});
