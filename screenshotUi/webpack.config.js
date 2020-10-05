const path = require('path');
const { VueLoaderPlugin } = require("vue-loader");
const env = 'development'


module.exports = {
    entry: './src/main.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
        publicPath: '/dist/', // 通过devServer访问路径
        filename: 'build.js' // 打包后的文件名
    },
    // env: 'development',
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [
                    { loader: "style-loader" },
                    { loader: "css-loader" }
                ]
            },
            {
                test: /\.vue$/,
                use: [
                    { loader: "vue-loader" }
                ]
            },
            {
                test: /\.(png|jpg|jpeg|gif)$/,
                use: [
                    {
                        loader: 'file-loader',
                        options: {
                            esModule: false,
                            name:"image/[name].[ext]"
                        }
                    },
                ]
            },
            {
                test: /\.(ttf|TTF)$/,
                use: [
                    {
                        loader: 'file-loader',
                    },
                ]
            }
        ]
    },
    devServer: {
        historyApiFallback: true,
        overlay: true
    },
    mode: 'development',
    plugins: [
        new VueLoaderPlugin()
    ],
    resolve: {
        extensions: ['.js', '.vue', '.css'],
        alias: {
            'vue$': 'vue/dist/vue.esm.js',
            '@': path.resolve(__dirname, 'src')
        }
    }
};