# springboot 项目中使用 aes 在 java 与数据库之间进行数据加密与解密

java 中常用的加密算法有 DES、IDEA、RC2、RC4、SKIPJACK、RC5、AES 算法等。AES 加密算法在处理效率、安全性等方面综合性较好，单密钥处理起来也比较方便，下文主要针对 AES 来展开阐述。

## AES 算法简介

AES 技术是一种对称的分组加密技术，使用 128 位分组加密数据，提供比 WEP/TKIPS 的 RC4 算法更高的加密强度。AES 的加密码表和解密码表是分开的，并且支持子密钥加密，这种做法优于以前用一个特殊的密钥解密的做法。AES 算法支持任意分组大小，初始时间快。特别是它具有的并行性可以有效地利用处理器资源。

AES 具有应用范围广、等待时间短、相对容易隐藏、吞吐量高等优点，在性能等各方面都优于 WEP 算法。利用此算法加密，WLAN 的安全性将会获得大幅度提高。AES 算法已经在 802.11i 标准中得到最终确认，成为取代 WEP 的新一代的加密算法。但是由于 AES 算法对硬件要求比较高，因此 AES 无法通过在原有设备上升级固件实现，必须重新设计芯片。

## 场景

先说一下应用场景：

- 写入：Java 中正常可读的 bean，加密后写入关系型数据库，数据库中仅存储密文；
- 读取：java 内通过 jdbc 读取关系型数据库中的密文，解密后转为相应的 bean 供给其它服务使用；

手动在 java 和数据库交互加一个加密与解密的服务可以满足该场景的要求，但是作为一个喜欢偷懒的人不喜欢这种解决方案。查询了一堆资料后发现属性转换类`javax.persistence.AttributeConverter`可用于业务对象属性转换上，在转换方法内部写如加密和解密算法刚好可以解决该场景的要求。网上提供的使用`AttributeConverter`来进行类型转换的方案中，业务层多使用的是 jpa，目前没有找到使用 mybatis 的方案。下面详细介绍下具体实施方法。

## 加密工具类

AES 加密工具类来源与博客`https://blog.csdn.net/SpiderManSun/article/details/84942010`。

```
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;

import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.security.MessageDigest;
import java.util.Base64;

public class AESUtil {
    /**
     * 秘钥：请勿修改
     */
    public static String key = "%%%*^@&^(!&$%^$(*((*sad131fe21";
    /**
     * AES加密
     *
     * @param plaintext   明文
     * @param Key         密钥
     * @param EncryptMode AES加密模式，CBC或ECB
     * @return 该字符串的AES密文值
     */
    public static String AESEncrypt(Object plaintext, String Key, String EncryptMode) {
        String PlainText = null;
        try {
            PlainText = plaintext.toString();
            if (Key == null) {
                return null;
            }
            Key = getMD5(Key);
            byte[] raw = Key.getBytes("utf-8");
            SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
            Cipher cipher = Cipher.getInstance("AES/" + EncryptMode + "/PKCS5Padding");
            if (EncryptMode == "ECB") {
                cipher.init(Cipher.ENCRYPT_MODE, skeySpec);
            } else {
                IvParameterSpec iv = new IvParameterSpec(Key.getBytes("utf-8"));//使用CBC模式，需要一个向量iv，可增加加密算法的强度
                cipher.init(Cipher.ENCRYPT_MODE, skeySpec, iv);
            }
            byte[] encrypted = cipher.doFinal(PlainText.getBytes("utf-8"));
            String encryptedStr = new String(new BASE64Encoder().encode(encrypted));
            return encryptedStr;
            //return new String(encrypted);//此处使用BASE64做转码功能，同时能起到2次加密的作用。
        } catch (Exception ex) {
            System.out.println(ex.toString());
            return null;
        }
    }

    /**
     * AES解密
     *
     * @param cipertext   密文
     * @param Key         密钥
     * @param EncryptMode AES加密模式，CBC或ECB
     * @return 该密文的明文
     */
    public static String AESDecrypt(Object cipertext, String Key, String EncryptMode) {
        String CipherText = null;
        try {
            CipherText = cipertext.toString();
            // 判断Key是否正确
            if (Key == null) {
                //System.out.print("Key为空null");
                return null;
            }
            Key = getMD5(Key);
            byte[] raw = Key.getBytes("utf-8");
            SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
            Cipher cipher = Cipher.getInstance("AES/" + EncryptMode + "/PKCS5Padding");
            if (EncryptMode == "ECB") {
                cipher.init(Cipher.DECRYPT_MODE, skeySpec);
            } else {
                IvParameterSpec iv = new IvParameterSpec(Key.getBytes("utf-8"));//使用CBC模式，需要一个向量iv，可增加加密算法的强度
                cipher.init(Cipher.DECRYPT_MODE, skeySpec, iv);
            }
            byte[] encrypted1 = new BASE64Decoder().decodeBuffer(CipherText);//先用base64解密
            //byte[] encrypted1 = CipherText.getBytes();
            try {
                byte[] original = cipher.doFinal(encrypted1);
                String originalString = new String(original, "utf-8");
                return originalString;
            } catch (Exception e) {
                System.out.println(e.toString());
                return null;
            }
        } catch (Exception ex) {
            System.out.println(ex.toString());
            return null;
        }
    }

    /**
     * 进行MD5加密
     *
     * @param s 要进行MD5转换的字符串
     * @return 该字符串的MD5值的8-24位
     */
    public static String getMD5(String s) {
        char hexDigits[] = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F'};

        try {
            byte[] btInput = s.getBytes();
            // 获得MD5摘要算法的 MessageDigest 对象
            MessageDigest mdInst = MessageDigest.getInstance("MD5");
            // 使用指定的字节更新摘要
            mdInst.update(btInput);
            // 获得密文
            byte[] md = mdInst.digest();
            // 把密文转换成十六进制的字符串形式
            int j = md.length;
            char str[] = new char[j * 2];
            int k = 0;
            for (int i = 0; i < j; i++) {
                byte byte0 = md[i];
                str[k++] = hexDigits[byte0 >>> 4 & 0xf];
                str[k++] = hexDigits[byte0 & 0xf];
            }
            return new String(str).substring(8, 24);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}

```

类中的私有变量 key 为 AES 密钥，一般可以视情况找地方存放。

## 属性类型转换器

- double 类型加密

```
import jdk.nashorn.internal.runtime.regexp.joni.exception.ValueException;

import javax.persistence.AttributeConverter;

public class DoubleFStringEncryptConverter implements AttributeConverter<Double, String> {

    @Override
    public String convertToDatabaseColumn(Double attribute) {
        return AESUtil.AESEncrypt(attribute, AESUtil.key, "CBC");
    }

    @Override
    public Double convertToEntityAttribute(String dbData) {
        String tmp = AESUtil.AESDecrypt(dbData, AESUtil.key, "CBC");
        Double value = Double.valueOf(-1);
        try {
            value = Double.valueOf(tmp);
        } catch (Exception ex) {
            ex.printStackTrace();
            throw new ValueException("字符串转换为浮点数失败");
        }
        return value;
    }
}

```

- int 类型加密

```
import jdk.nashorn.internal.runtime.regexp.joni.exception.ValueException;

import javax.persistence.AttributeConverter;

public class IntegerFStringEncryptConverter implements AttributeConverter<Integer, String> {

    @Override
    public String convertToDatabaseColumn(Integer attribute) {
        return AESUtil.AESEncrypt(attribute, AESUtil.key, "CBC");
    }

    @Override
    public Integer convertToEntityAttribute(String dbData) {
        String tmp = AESUtil.AESDecrypt(dbData, AESUtil.key, "CBC");
        Integer value = Integer.valueOf(-1);
        try {
            value = Integer.valueOf(tmp);
        } catch (Exception ex) {
            ex.printStackTrace();
            throw new ValueException("字符串转换为整数失败");
        }
        return value;
    }
}
```

- String 类型加密

```
import javax.persistence.AttributeConverter;

public class StringFStringEncryptConverter implements AttributeConverter<String, String> {
    @Override
    public String convertToDatabaseColumn(String attribute) {
        return AESUtil.AESEncrypt(attribute, AESUtil.key, "CBC");
    }

    @Override
    public String convertToEntityAttribute(String dbData) {
        return AESUtil.AESDecrypt(dbData, AESUtil.key, "CBC");
    }
}
```

## 转换器在 Entity 中的使用

```
import lombok.Data;

import javax.persistence.*;
import java.io.Serializable;

@Data
@Entity
@Table(name = "t_test")
public class CityBaseInfoPo implements Serializable {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name="id")
    private Integer id;

    @Convert(converter = StringFStringEncryptConverter.class)
    @Column(name = "city_id")
    private String cityId;

    @Column(name = "angle")
    @Convert(converter = DoubleFStringEncryptConverter.class)
    private double angle;

    @Column(name = "height_above_sea")
    @Convert(converter = DoubleFStringEncryptConverter.class)
    private double heightAboveSea;

    @Column(name = "latitude")
    @Convert(converter = DoubleFStringEncryptConverter.class)
    private double latitude;

    @Column(name = "longitude")
    @Convert(converter = DoubleFStringEncryptConverter.class)
    private double longitude;
}
```

## 加密效果

![img1](<./1588239124(1).png>)
