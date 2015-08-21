#include "formfiller.h"
#include "maintask.h"

#include <QtDebug>
#include <QCoreApplication>

#include <poppler-form.h>

FormFiller::FormFiller(QString fileName, QObject *parent) :
    QObject(parent),
    fileName(fileName),
    document(Poppler::Document::load(fileName))
{
    if (document == NULL) {
        MainTask::fail("Document file could not be open");
    }
}

FieldInfo* fieldInfoFromField(const Poppler::FormField* field, int pageNumber) {
    switch(field->type()) {
        case Poppler::FormField::FormText:
            return new FieldInfo(pageNumber,
                                 "text",
                                 field->fullyQualifiedName(),
                                 ((Poppler::FormFieldText *)field)->text());
        case Poppler::FormField::FormButton: {
            QString type;
            Poppler::FormFieldButton* button = (Poppler::FormFieldButton*)field;
            switch(button->buttonType()) {
                case Poppler::FormFieldButton::CheckBox:
                    type = "check";
                    break;
                case Poppler::FormFieldButton::Radio:
                    type = "radio";
                    break;
                case Poppler::FormFieldButton::Push:
                    type = "push";
                    break;
            }
            return new FieldInfo(pageNumber,
                                 type,
                                 field->fullyQualifiedName(),
                                 button->state());
        }
        default:
            break;
    }
    return NULL;
}


QList<FieldInfo *> FormFiller::listFieldsInfo()
{
    QList<FieldInfo *> output;
    int n = document->numPages();

    for (int i = 0; i < n; i += 1) {
        Poppler::Page *page = document->page(i);

        foreach (Poppler::FormField *field, page->formFields()) {
            if (!field->isReadOnly() && field->isVisible()) {
                FieldInfo* fieldInfo = fieldInfoFromField(field, i);
                if (fieldInfo) {
                    output << fieldInfo;
                }
            }
        }
    }

    return output;
}

void FormFiller::fill(const QMap<QString, FieldInfo *> &fieldsInfo)
{
    int n = document->numPages();

    for (int i = 0; i < n; i += 1) {
        Poppler::Page *page = document->page(i);

        foreach(Poppler::FormField *field, page->formFields()) {
            QString name = field->fullyQualifiedName();

            if (!field->isReadOnly()
                    && field->isVisible()
                    && fieldsInfo.contains(name)) {
                FieldInfo *info = fieldsInfo[name];

                if (field->type() == Poppler::FormField::FormText
                        && info->getType() == "text") {
                    Poppler::FormFieldText *textField = (Poppler::FormFieldText *) field;
                    textField->setText(info->getValue().toString());
                }
                if (field->type() == Poppler::FormField::FormButton
                        && info->getType() == "check") {
                    Poppler::FormFieldButton *buttonField = (Poppler::FormFieldButton *) field;
                    bool value = info->getValue().toBool();
                    buttonField->setState(value);
                }
            }
        }
    }
}

void FormFiller::save(const QString &fileName)
{
    Poppler::PDFConverter *converter = document->pdfConverter();
    converter->setOutputFileName(fileName);
    converter->setPDFOptions(converter->pdfOptions() | Poppler::PDFConverter::WithChanges);

    if (!converter->convert()) {
        MainTask::fail("Saving output failed");
    }
}
