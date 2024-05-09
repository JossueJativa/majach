// Obtener referencia al botón
const filterButton = document.querySelector('button[type="button"]');

// Adjuntar un evento de clic al botón
filterButton.addEventListener('click', async () => {
    try {
        await initChart_products();
        await initChart_stars();
    } catch (error) {
        throw new Error(error);
    }
});

const initChart_stars = async () => {
    try {
        const myChart = echarts.init(document.getElementById('chart5'));
        const starsData = await getOptionsStarsProducts(); // Agrega aquí la llamada a getOptionsStarsProducts()
        myChart.setOption(starsData);
        myChart.resize();
    } catch (error) {
        throw new Error(error);
    }
}

const getOptionsStarsProducts = async() => {
    const start_date = document.getElementById('start_date').value; // Asegúrate de obtener start_date y end_date aquí
    const end_date = document.getElementById('end_date').value;

    try{
        const response = await fetch(`http://127.0.0.1:8000/get_products_stars/${start_date}/${end_date}/`);
        const data = await response.json();
        return data;
    } catch (error) {
        throw new Error(error);
    }
}



const getOptionProducts = async () => {
    start_date = document.getElementById('start_date').value;
    end_date = document.getElementById('end_date').value;

    try {
        const response = await fetch(`http://127.0.0.1:8000/get_products/${start_date}/${end_date}/`);
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
        const [favoritesData, sellerData, cartData] = await Promise.all([
            getOptionFavorites(),
            getOptionSellers(),
            getOptionCart(),
        ]);
        initChart_favorites(favoritesData);
        initChart_sellers(sellerData);
        initChart_cart(cartData);
    } catch (error) {
    }
});
