#include "widget.h"
#include <QApplication>
#include <QIcon>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    Widget w;
    w.setWindowTitle("SteamRush");
    a.setWindowIcon(QIcon("./icon/icons8-steam-64.png"));
    w.show();


    return a.exec();
}
