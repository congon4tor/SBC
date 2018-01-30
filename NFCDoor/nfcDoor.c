#include <stdlib.h>
#include <nfc/nfc.h>
#include <mraa.h>
#include <string.h>
#include <json-c/json.h>
#include "peticionesHttp.h"
#include <unistd.h>

nfc_device *pnd;
nfc_target nt;
nfc_context *context;
mraa_i2c_context i2c;
const int ledR=11,ledG=18,ledB=16; 
mraa_gpio_context gpR,gpG,gpB;
uint8_t uid[4];
char cod_uid[4];
char nombreSala[10], aforoAct[2], aforoMax[2],menInicio[]="Acerque su tarjeta",menBienvenida[]="Bienvenido ", nombreAsistente[20],menError[20];
const nfc_modulation nmMifare = {
    .nmt = NMT_ISO14443A,
    .nbr = NBR_106,
};


static void convertirUid(){
  sprintf(cod_uid,"%02X %02X %02X %02X",uid[0],uid[1],uid[2],uid[3]);
  //printf("\nEsta accediendo: %s\n",cod_uid);
}


void espacio(int num){
      int i;
      for (i=0;i<num;i++){
        mraa_i2c_write_byte_data(i2c,0x4A,0xFE);
        sleep(0.1);
      }
}
 void setCursor(int linea, int pos){
  int pos_new;
  if (linea == 1)
        pos_new = pos;
  else if (linea == 2)
        pos_new = 0x40 + pos;        
  else if (linea == 3)
        pos_new = 0x14 + pos;
  else if (linea == 4)
        pos_new = 0x54 + pos;

  mraa_i2c_write_byte_data(i2c,0x45,0xFE);
  sleep(0.1);
  mraa_i2c_write_byte(i2c,pos_new);
  sleep(0.1);
 }

void ledRGB(int R, int G, int B){
  gpR=mraa_gpio_init(ledR);
  mraa_gpio_dir(gpR,MRAA_GPIO_OUT);
  gpG=mraa_gpio_init(ledG);
  mraa_gpio_dir(gpG,MRAA_GPIO_OUT);
  gpB=mraa_gpio_init(ledB);
  mraa_gpio_dir(gpB,MRAA_GPIO_OUT);

  mraa_gpio_write(gpR,R);
  mraa_gpio_write(gpB,B);
  mraa_gpio_write(gpG,G);

  mraa_gpio_close(gpR);
  mraa_gpio_close(gpB);
  mraa_gpio_close(gpG);
}

static void clean_screen(){
  mraa_i2c_write_byte_data(i2c,0x51,0xFE);
  sleep(0.02);
}

void print_info_general(){
     int i;
    //printf("\n%s\n",nombreSala);
     for (i=0;i<strlen(nombreSala);i++){
        mraa_i2c_write_byte(i2c,nombreSala[i]);
        sleep(0.02);
        
     }
     espacio(15-strlen(nombreSala));

     for (i=0;i<strlen(aforoAct);i++){
        mraa_i2c_write_byte(i2c,aforoAct[i]);
        sleep(0.02);
     }

     mraa_i2c_write_byte(i2c,0x2F);
        sleep(0.02);
     for (i=0;i<strlen(aforoMax);i++){
        mraa_i2c_write_byte(i2c,aforoMax[i]);
        sleep(0.02);
     }
    setCursor(3,0);
    for (i=0;i<strlen(menInicio);i++){
        mraa_i2c_write_byte(i2c,menInicio[i]);
        sleep(0.02);
     }     

}

static size_t tryAccessCallback(void *contents, size_t size, size_t nmemb, void *userp){
  size_t realsize = size * nmemb;                                                     
  struct json_object *obj;
  
  obj = json_tokener_parse(contents);                                             
  if(obj != NULL) {
      struct json_object* returnObj;
      struct json_object* returnObj2;
      struct json_object* returnObj3;
      struct json_object* returnObj4;
      returnObj = json_object_object_get(obj, "response");
      char success[20];
      strcpy(success, "success");
      if(strcmp(json_object_get_string(returnObj), success)==0){
          int i;
          //Acceso a sala realizado con exito
          //TODO: Abrir puerta, hacer sonido, mensaje de bienvenida, encender led verde
          ledRGB(0,1,0);
          returnObj2=json_object_object_get(obj, "nombre");
          returnObj3=json_object_object_get(obj, "aforo");
          strcpy(nombreAsistente,json_object_get_string(returnObj2));
          strcpy(aforoAct,json_object_get_string(returnObj3));
          clean_screen();
          for (i=0;i<strlen(menBienvenida);i++){
             mraa_i2c_write_byte(i2c,menBienvenida[i]);
             sleep(0.02);
          }     
           for (i=0;i<strlen(nombreAsistente);i++){
             mraa_i2c_write_byte(i2c,nombreAsistente[i]);
             sleep(0.02);
          }    

          // json_object_object_foreach(obj, key, val) {                                 
          //   printf("%s ==> %s\n",key, json_object_get_string(val));       
          // } 
      }else{
          //Fallo al intentar el acceso
          //TODO: Hacer sonido, mensaje de error, encender led rojo
          int i;
          //ledRGB(1,0,0);
          returnObj4=json_object_object_get(obj, "error");
          strcpy(menError,json_object_get_string(returnObj4));
          clean_screen();
           for (i=0;i<strlen(menError);i++){
             mraa_i2c_write_byte(i2c,menError[i]);
             sleep(0.02);
          }    
      }
  }
  
  /* free json object */
  json_object_put(obj);

  return realsize;  //HAy que devolver esto si o si por temas de la libreria
}

static size_t getRoomDataCallback(void *contents, size_t size, size_t nmemb, void *userp){
  size_t realsize = size * nmemb;                                                     
  struct json_object *obj;
  
  obj = json_tokener_parse(contents);                                             
  if(obj != NULL) {
      struct json_object* returnObj;
      struct json_object* returnObj2;
      struct json_object* returnObj3;
      returnObj = json_object_object_get(obj, "response");
      char success[20];
      strcpy(success, "success");
      if(strcmp(json_object_get_string(returnObj), success)==0){
          returnObj = json_object_object_get(obj, "nombre");
          strcpy(nombreSala,json_object_get_string(returnObj));
          returnObj2 = json_object_object_get(obj, "aforo_act");
          strcpy(aforoAct,json_object_get_string(returnObj2));
          returnObj3 = json_object_object_get(obj, "aforo_max");
          strcpy(aforoMax,json_object_get_string(returnObj3));
          
          print_info_general();
        //  json_object_object_foreach(obj, key, val) {                                 
        //    printf("%s ==> %s\n",key, json_object_get_string(val));       
        //   } 
      }else{
        int i;
        char error[]="Error al recorger datos";
        for (i=0;i<strlen(error);i++){
          mraa_i2c_write_byte(i2c,error[i]);
          sleep(0.02);
        }

          json_object_object_foreach(obj, key, val) {                                 
            printf("%s ==> %s\n",key, json_object_get_string(val));       
          } 
      }
  }
  
  /* free json object */
  json_object_put(obj);

  return realsize;  //HAy que devolver esto si o si por temas de la libreria
}


static void init(){
  //init nfc
  nfc_init(&context);
  if (context == NULL) {
    printf("Unable to init libnfc (malloc)\n");
    exit(EXIT_FAILURE);
  }
  
  pnd = nfc_open(context, "pn532_i2c:/dev/i2c-4");
  if (pnd == NULL) {
    printf("ERROR: %s\n", "Unable to open NFC device.");
    exit(EXIT_FAILURE);
  }
  if (nfc_initiator_init(pnd) < 0) {
    nfc_perror(pnd, "nfc_initiator_init");
    exit(EXIT_FAILURE);
  }
  printf("NFC reader: %s opened\n", nfc_device_get_name(pnd));

  //init i2c for lcd
  i2c = mraa_i2c_init(0);
  mraa_i2c_address(i2c, 0x10);
  mraa_i2c_write_byte_data(i2c,0x48,0xFE);
  sleep(0.02);
  mraa_i2c_write_byte_data(i2c,0x4C,0xFE);
  sleep(0.02);
  clean_screen();
  
  getRoomData(getRoomDataCallback);

  //init LED
 
  

  ledRGB(0,0,1);

}






static void print_info_keypad(){
    //todo
    //codigo:****

}

 void wait_nfc(nfc_device *pnd,nfc_target nt){
  if (nfc_initiator_select_passive_target(pnd, nmMifare, NULL, 0, &nt) > 0) {
    strcpy(uid,nt.nti.nai.abtUid);
    convertirUid();
    tryAccess(tryAccessCallback,cod_uid);
    
  }
  
}
 
static void req_infoSala(){

} 

static void req_access(){

}

static void req_exit(){

}

static void set_led(){

}

static void set_zumbador(){

}

static void read_keypad(){
    
}


int main(int argc, const char *argv[]){
  init();  

  while(1){
  wait_nfc(pnd,nt);
  sleep(2);
  clean_screen();
  sleep(1);
  ledRGB(0,0,1);
  print_info_general();
  }
 
  
  nfc_close(pnd);
  nfc_exit(context);
  exit(EXIT_SUCCESS);
}
