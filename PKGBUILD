# Maintainer: tiredamphibian <gwen.madeleine77@gmail.com>
pkgname=pinetree
pkgver=1.0
pkgrel=1
pkgdesc="Pinetree Audio Converter"
arch=('any')
url="https://example.com"
license=('GPL')
depends=('python' 'ffmpeg' 'ncurses')
source=("pinetree.py")
install=.install
sha256sums=('SKIP')

package() {
    install -Dm755 "$srcdir/pinetree.py" "$pkgdir/usr/bin/pinetree"
    install -d "$pkgdir/usr/share/pinetree"
}
