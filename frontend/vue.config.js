const path = require('path');
const CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: process.env.VUE_APP_API_URL || 'http://localhost:3000',
        changeOrigin: true,
        pathRewrite: {
          '^/api': ''
        }
      }
    }
  },
  configureWebpack: {
    plugins: [
      new CopyWebpackPlugin({
        patterns: [
          {
            from: path.resolve(__dirname, 'node_modules/ketcher-react/dist/'),
            to: path.resolve(__dirname, 'dist/ketcher/'),
            globOptions: {
              ignore: ['**/ketcher.html']
            }
          }
        ]
      })
    ]
  }
}