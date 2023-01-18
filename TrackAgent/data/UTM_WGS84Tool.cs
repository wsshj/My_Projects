#region UTM_WGS84Tool
// **********************************************************************
//Copyright(C) 2021 by 北京北方新视野  All rights reserved
//作者:           薛朝阳
//软件版本：      2018.4.17f1
//日期:           2021-08-31 17:22:09
//功能描述:       UTM_WGS84Tool
// **********************************************************************
#endregion

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using UnityEngine;

public class UTM_WGS84Tool
{
    static double pi = Math.PI;

    /* Ellipsoid model constants (actual values here are for WGS84) */
    static double sm_a = 6378137.0;
    static double sm_b = 6356752.314;
    static double sm_EccSquared = 6.69437999013e-03;

    static double UTMScaleFactor = 0.9996;
    
    //地图上的宽度 对应到三维世界中需要成的系数
    public static double coefficientX = 2075.0 / 11564.0;

    //地图上的高度 对应到三维世界中需要成的系数
    public static double coefficientY = 2773.0 / 15218.0;

    public static Vector3 center = new Vector3(1347,0 ,2437);


    /*
    * DegToRad
    *
    * Converts degrees to radians.
    *
    */
    private static double DegToRad(double deg)
    {
        return (deg / 180.0 * pi);
    }




    /*
    * RadToDeg
    *
    * Converts radians to degrees.
    *
    */
    private static double RadToDeg(double rad)
    {
        return (rad / pi * 180.0);
    }




    /*
    * ArcLengthOfMeridian
    *
    * Computes the ellipsoidal distance from the equator to a point at a
    * given latitude.
    *
    * Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
    * GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
    *
    * Inputs:
    *     phi - Latitude of the point, in radians.
    *
    * Globals:
    *     sm_a - Ellipsoid model major axis.
    *     sm_b - Ellipsoid model minor axis.
    *
    * Returns:
    *     The ellipsoidal distance of the point from the equator, in meters.
    *
    */
    private static double ArcLengthOfMeridian(double phi)
    {
        double alpha, beta, gamma, delta, epsilon, n;
        double result;

        /* Precalculate n */
        n = (sm_a - sm_b) / (sm_a + sm_b);

        /* Precalculate alpha */
        alpha = ((sm_a + sm_b) / 2.0)
           * (1.0 + (Math.Pow(n, 2.0) / 4.0) + (Math.Pow(n, 4.0) / 64.0));

        /* Precalculate beta */
        beta = (-3.0 * n / 2.0) + (9.0 * Math.Pow(n, 3.0) / 16.0)
           + (-3.0 * Math.Pow(n, 5.0) / 32.0);

        /* Precalculate gamma */
        gamma = (15.0 * Math.Pow(n, 2.0) / 16.0)
            + (-15.0 * Math.Pow(n, 4.0) / 32.0);

        /* Precalculate delta */
        delta = (-35.0 * Math.Pow(n, 3.0) / 48.0)
            + (105.0 * Math.Pow(n, 5.0) / 256.0);

        /* Precalculate epsilon */
        epsilon = (315.0 * Math.Pow(n, 4.0) / 512.0);

        /* Now calculate the sum of the series and return */
        result = alpha
            * (phi + (beta * Math.Sin(2.0 * phi))
                + (gamma * Math.Sin(4.0 * phi))
                + (delta * Math.Sin(6.0 * phi))
                + (epsilon * Math.Sin(8.0 * phi)));

        return result;
    }



    /*
    * UTMCentralMeridian
    *
    * Determines the central meridian for the given UTM zone.
    *
    * Inputs:
    *     zone - An integer value designating the UTM zone, range [1,60].
    *
    * Returns:
    *   The central meridian for the given UTM zone, in radians, or zero
    *   if the UTM zone parameter is outside the range [1,60].
    *   Range of the central meridian is the radian equivalent of [-177,+177].
    *
    */
    private static double UTMCentralMeridian(double zone)
    {
        double cmeridian;

        cmeridian = DegToRad(-183.0 + (zone * 6.0));

        return cmeridian;
    }



    /*
    * FootpointLatitude
    *
    * Computes the footpoint latitude for use in converting transverse
    * Mercator coordinates to ellipsoidal coordinates.
    *
    * Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
    *   GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
    *
    * Inputs:
    *   y - The UTM northing coordinate, in meters.
    *
    * Returns:
    *   The footpoint latitude, in radians.
    *
    */
    private static double FootpointLatitude(double y)
    {
        double y_, alpha_, beta_, gamma_, delta_, epsilon_, n;
        double result;

        /* Precalculate n (Eq. 10.18) */
        n = (sm_a - sm_b) / (sm_a + sm_b);

        /* Precalculate alpha_ (Eq. 10.22) */
        /* (Same as alpha in Eq. 10.17) */
        alpha_ = ((sm_a + sm_b) / 2.0)
            * (1 + (Math.Pow(n, 2.0) / 4) + (Math.Pow(n, 4.0) / 64));

        /* Precalculate y_ (Eq. 10.23) */
        y_ = y / alpha_;

        /* Precalculate beta_ (Eq. 10.22) */
        beta_ = (3.0 * n / 2.0) + (-27.0 * Math.Pow(n, 3.0) / 32.0)
            + (269.0 * Math.Pow(n, 5.0) / 512.0);

        /* Precalculate gamma_ (Eq. 10.22) */
        gamma_ = (21.0 * Math.Pow(n, 2.0) / 16.0)
            + (-55.0 * Math.Pow(n, 4.0) / 32.0);

        /* Precalculate delta_ (Eq. 10.22) */
        delta_ = (151.0 * Math.Pow(n, 3.0) / 96.0)
            + (-417.0 * Math.Pow(n, 5.0) / 128.0);

        /* Precalculate epsilon_ (Eq. 10.22) */
        epsilon_ = (1097.0 * Math.Pow(n, 4.0) / 512.0);

        /* Now calculate the sum of the series (Eq. 10.21) */
        result = y_ + (beta_ * Math.Sin(2.0 * y_))
            + (gamma_ * Math.Sin(4.0 * y_))
            + (delta_ * Math.Sin(6.0 * y_))
            + (epsilon_ * Math.Sin(8.0 * y_));

        return result;
    }



    /*
    * MapLatLonToXY
    *
    * Converts a latitude/longitude pair to x and y coordinates in the
    * Transverse Mercator projection.  Note that Transverse Mercator is not
    * the same as UTM; a scale factor is required to convert between them.
    *
    * Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
    * GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
    *
    * Inputs:
    *    phi - Latitude of the point, in radians.
    *    lambda - Longitude of the point, in radians.
    *    lambda0 - Longitude of the central meridian to be used, in radians.
    *
    * Outputs:
    *    xy - A 2-element array containing the x and y coordinates
    *         of the computed point.
    *
    * Returns:
    *    The function does not return a value.
    *
    */
    private static void MapLatLonToXY(double phi, double lambda, double lambda0, out double[] xy)
    {
        double N, nu2, ep2, t, t2, l;
        double l3coef, l4coef, l5coef, l6coef, l7coef, l8coef;
        double tmp;

        /* Precalculate ep2 */
        ep2 = (Math.Pow(sm_a, 2.0) - Math.Pow(sm_b, 2.0)) / Math.Pow(sm_b, 2.0);

        /* Precalculate nu2 */
        nu2 = ep2 * Math.Pow(Math.Cos(phi), 2.0);

        /* Precalculate N */
        N = Math.Pow(sm_a, 2.0) / (sm_b * Math.Sqrt(1 + nu2));

        /* Precalculate t */
        t = Math.Tan(phi);
        t2 = t * t;
        tmp = (t2 * t2 * t2) - Math.Pow(t, 6.0);

        /* Precalculate l */
        l = lambda - lambda0;

        /* Precalculate coefficients for l**n in the equations below
           so a normal human being can read the expressions for easting
           and northing
           -- l**1 and l**2 have coefficients of 1.0 */
        l3coef = 1.0 - t2 + nu2;

        l4coef = 5.0 - t2 + 9 * nu2 + 4.0 * (nu2 * nu2);

        l5coef = 5.0 - 18.0 * t2 + (t2 * t2) + 14.0 * nu2
            - 58.0 * t2 * nu2;

        l6coef = 61.0 - 58.0 * t2 + (t2 * t2) + 270.0 * nu2
            - 330.0 * t2 * nu2;

        l7coef = 61.0 - 479.0 * t2 + 179.0 * (t2 * t2) - (t2 * t2 * t2);

        l8coef = 1385.0 - 3111.0 * t2 + 543.0 * (t2 * t2) - (t2 * t2 * t2);

        xy = new double[2];
        /* Calculate easting (x) */
        xy[0] = N * Math.Cos(phi) * l
            + (N / 6.0 * Math.Pow(Math.Cos(phi), 3.0) * l3coef * Math.Pow(l, 3.0))
            + (N / 120.0 * Math.Pow(Math.Cos(phi), 5.0) * l5coef * Math.Pow(l, 5.0))
            + (N / 5040.0 * Math.Pow(Math.Cos(phi), 7.0) * l7coef * Math.Pow(l, 7.0));

        /* Calculate northing (y) */
        xy[1] = ArcLengthOfMeridian(phi)
            + (t / 2.0 * N * Math.Pow(Math.Cos(phi), 2.0) * Math.Pow(l, 2.0))
            + (t / 24.0 * N * Math.Pow(Math.Cos(phi), 4.0) * l4coef * Math.Pow(l, 4.0))
            + (t / 720.0 * N * Math.Pow(Math.Cos(phi), 6.0) * l6coef * Math.Pow(l, 6.0))
            + (t / 40320.0 * N * Math.Pow(Math.Cos(phi), 8.0) * l8coef * Math.Pow(l, 8.0));

        return;
    }



    /*
    * MapXYToLatLon
    *
    * Converts x and y coordinates in the Transverse Mercator projection to
    * a latitude/longitude pair.  Note that Transverse Mercator is not
    * the same as UTM; a scale factor is required to convert between them.
    *
    * Reference: Hoffmann-Wellenhof, B., Lichtenegger, H., and Collins, J.,
    *   GPS: Theory and Practice, 3rd ed.  New York: Springer-Verlag Wien, 1994.
    *
    * Inputs:
    *   x - The easting of the point, in meters.
    *   y - The northing of the point, in meters.
    *   lambda0 - Longitude of the central meridian to be used, in radians.
    *
    * Outputs:
    *   philambda - A 2-element containing the latitude and longitude
    *               in radians.
    *
    * Returns:
    *   The function does not return a value.
    *
    * Remarks:
    *   The local variables Nf, nuf2, tf, and tf2 serve the same purpose as
    *   N, nu2, t, and t2 in MapLatLonToXY, but they are computed with respect
    *   to the footpoint latitude phif.
    *
    *   x1frac, x2frac, x2poly, x3poly, etc. are to enhance readability and
    *   to optimize computations.
    *
    */
    private static void MapXYToLatLon(double x, double y, double lambda0, out double[] xy)
    {
        double phif, Nf, Nfpow, nuf2, ep2, tf, tf2, tf4, cf;
        double x1frac, x2frac, x3frac, x4frac, x5frac, x6frac, x7frac, x8frac;
        double x2poly, x3poly, x4poly, x5poly, x6poly, x7poly, x8poly;

        /* Get the value of phif, the footpoint latitude. */
        phif = FootpointLatitude(y);

        /* Precalculate ep2 */
        ep2 = (Math.Pow(sm_a, 2.0) - Math.Pow(sm_b, 2.0))
              / Math.Pow(sm_b, 2.0);

        /* Precalculate cos (phif) */
        cf = Math.Cos(phif);

        /* Precalculate nuf2 */
        nuf2 = ep2 * Math.Pow(cf, 2.0);

        /* Precalculate Nf and initialize Nfpow */
        Nf = Math.Pow(sm_a, 2.0) / (sm_b * Math.Sqrt(1 + nuf2));
        Nfpow = Nf;

        /* Precalculate tf */
        tf = Math.Tan(phif);
        tf2 = tf * tf;
        tf4 = tf2 * tf2;

        /* Precalculate fractional coefficients for x**n in the equations
           below to simplify the expressions for latitude and longitude. */
        x1frac = 1.0 / (Nfpow * cf);

        Nfpow *= Nf;   /* now equals Nf**2) */
        x2frac = tf / (2.0 * Nfpow);

        Nfpow *= Nf;   /* now equals Nf**3) */
        x3frac = 1.0 / (6.0 * Nfpow * cf);

        Nfpow *= Nf;   /* now equals Nf**4) */
        x4frac = tf / (24.0 * Nfpow);

        Nfpow *= Nf;   /* now equals Nf**5) */
        x5frac = 1.0 / (120.0 * Nfpow * cf);

        Nfpow *= Nf;   /* now equals Nf**6) */
        x6frac = tf / (720.0 * Nfpow);

        Nfpow *= Nf;   /* now equals Nf**7) */
        x7frac = 1.0 / (5040.0 * Nfpow * cf);

        Nfpow *= Nf;   /* now equals Nf**8) */
        x8frac = tf / (40320.0 * Nfpow);

        /* Precalculate polynomial coefficients for x**n.
           -- x**1 does not have a polynomial coefficient. */
        x2poly = -1.0 - nuf2;

        x3poly = -1.0 - 2 * tf2 - nuf2;

        x4poly = 5.0 + 3.0 * tf2 + 6.0 * nuf2 - 6.0 * tf2 * nuf2
            - 3.0 * (nuf2 * nuf2) - 9.0 * tf2 * (nuf2 * nuf2);

        x5poly = 5.0 + 28.0 * tf2 + 24.0 * tf4 + 6.0 * nuf2 + 8.0 * tf2 * nuf2;

        x6poly = -61.0 - 90.0 * tf2 - 45.0 * tf4 - 107.0 * nuf2
            + 162.0 * tf2 * nuf2;

        x7poly = -61.0 - 662.0 * tf2 - 1320.0 * tf4 - 720.0 * (tf4 * tf2);

        x8poly = 1385.0 + 3633.0 * tf2 + 4095.0 * tf4 + 1575 * (tf4 * tf2);
        xy = new double[2];

        /* Calculate longitude */
        xy[0] = lambda0 + x1frac * x
            + x3frac * x3poly * Math.Pow(x, 3.0)
            + x5frac * x5poly * Math.Pow(x, 5.0)
            + x7frac * x7poly * Math.Pow(x, 7.0);


        /* Calculate latitude */
        xy[1] = phif + x2frac * x2poly * (x * x)
            + x4frac * x4poly * Math.Pow(x, 4.0)
            + x6frac * x6poly * Math.Pow(x, 6.0)
            + x8frac * x8poly * Math.Pow(x, 8.0);


        return;
    }




    /*
    * LatLonToUTMXY
    *
    * Converts a latitude/longitude pair to x and y coordinates in the
    * Universal Transverse Mercator projection.
    *
    * Inputs:
    *   lat - Latitude of the point, in radians.
    *   lon - Longitude of the point, in radians.
    *   zone - UTM zone to be used for calculating values for x and y.
    *          If zone is less than 1 or greater than 60, the routine
    *          will determine the appropriate zone from the value of lon.
    *
    * Outputs:
    *   xy - A 2-element array where the UTM x and y values will be stored.
    *
    * Returns:
    *   The UTM zone used for calculating the values of x and y.
    *
    */
    public static double[] LatLonToUTMXY(double lon, double lat)
    {
        double zone = Math.Floor((lon + 180.0) / 6) + 1;
        double[] xy = new double[2];
        MapLatLonToXY(DegToRad(lat), DegToRad(lon), UTMCentralMeridian(zone), out xy);

        /* Adjust easting and northing for UTM system. */
        xy[0] = xy[0] * UTMScaleFactor + 500000.0;
        xy[1] = xy[1] * UTMScaleFactor;
        if (xy[1] < 0.0)
            xy[1] = xy[1] + 10000000.0;

        return new double[] { xy[0], xy[1], zone };
    }



    /*
    * UTMXYToLatLon
    *
    * Converts x and y coordinates in the Universal Transverse Mercator
    * projection to a latitude/longitude pair.
    *
    * Inputs:
    *	x - The easting of the point, in meters.
    *	y - The northing of the point, in meters.
    *	zone - The UTM zone in which the point lies.
    *	southhemi - True if the point is in the southern hemisphere;
    *               false otherwise.
    *
    * Outputs:
    *	latlon - A 2-element array containing the latitude and
    *            longitude of the point, in radians.
    *
    * Returns:
    *	The function does not return a value.
    *
    */
    // zone - 50    southhemi - true
    public static double[] UTMXYToLatLon(double x, double y, double zone, bool southhemi)
    {
        double cmeridian;

        x -= 500000.0;
        x /= UTMScaleFactor;

        /* If in southern hemisphere, adjust y accordingly. */
        if (southhemi)
            y -= 10000000.0;

        y /= UTMScaleFactor;

        cmeridian = UTMCentralMeridian(zone);
        double[] xy = new double[2];
        MapXYToLatLon(x, y, cmeridian, out xy);
        xy[0] = RadToDeg(xy[0]);
        xy[1] = RadToDeg(xy[1]);
        return xy;
    }

    /// <summary>
    /// 经度
    /// </summary>
    private static double _longitude
    {
        get
        {
            return Constant.Config.BASE_LONGITUDE;
        }
    }
    /// <summary>
    /// 纬度
    /// </summary>
    private static double _latitude
    {
        get
        {
            return Constant.Config.BASE_LATITUDE;
        }
    }

    /// <summary>
    /// 大地坐标 -  X 基准坐标
    /// </summary>
    public double _utm_x
    {
        get
        {
            return LatLonToUTMXY(_longitude, _latitude)[0];
        }
    }
    /// <summary>
    /// 大地坐标 -  Y 基准坐标
    /// </summary>
    public double _utm_y
    {
        get
        {
            return LatLonToUTMXY(_longitude, _latitude)[1];
        }
    }

    /// <summary>
    /// 空间位置
    /// </summary>
    public double _zone
    {
        get
        {
            return LatLonToUTMXY(_longitude, _latitude)[2];
        }
    }

    /// <summary>
    /// 通过经纬度获取 Unity 2D坐标(不含高度)
    /// </summary>
    /// <param name="point"><see cref="Point2"/>对象, 对经纬度的封装</param>
    /// <returns></returns>
    public static Vector2 ToVector(Point2 point)
    {
        double _x = ((point.longitude - 122.136829994473) * 85034.617864360044246411962685833 + 2140);
        double _y = -((point.latitude - 37.4688299967702) * -103627.52438550783120400193244459 + 8312) + 7609;
        return new Vector2((float)_x, (float)_y);

        //double[] curent = LatLonToUTMXY(point.longitude, point.latitude);
        //double[] center = LatLonToUTMXY(_longitude, _latitude);
        //double _x = center[0] - curent[0];
        //double _y = center[1] - curent[1];
        //return new Vector2((float)_x, (float)_y);
    }

    /// <summary>
    /// 通过经纬度获取 Unity 2D坐标(2维平面坐标 不含高度)
    /// </summary>
    /// <param name="longitude">经度</param>
    /// <param name="latitude">纬度</param>
    /// <returns></returns>
    public static Vector2 ToVector(double longitude, double latitude)
    {
        double _x = ((longitude - 122.136829994473) * 85034.617864360044246411962685833 + 2140);
        double _y = -((latitude - 37.4688299967702) * -103627.52438550783120400193244459 + 8312) + 7609;
        return new Vector2((float)_x, (float)_y);
        //double[] curent = LatLonToUTMXY(longitude, latitude);
        //double[] center = LatLonToUTMXY(_longitude, _latitude);
        //double _x = center[0] - curent[0];
        //double _y = center[1] - curent[1];
        //return new Vector2((float)_x, (float)_y);
    }

    /// <summary>
    /// 通过经纬高度获取 Unity 3D坐标(含高度)
    /// </summary>
    /// <param name="point"><see cref="Point3"/>对象, 对经纬高数据的封装</param>
    /// <returns></returns>
    public static Vector3 ToVector(Point3 point)
    {
        double _x = ((point.longitude - 122.136829994473) * -85369.821291030713527972595556599 - 1809.04);
        double _y = ((point.latitude - 37.4688299967702) * -103620.81635379537645599988767665 + 4227.987);
        return new Vector3((float)_x, (float)point.height,(float)_y);
        //double[] current = LatLonToUTMXY(point.longitude, point.latitude);
        //double[] center = LatLonToUTMXY(_longitude, _latitude);
        //double _x = center[0] - current[0];
        //double _y = center[1] - current[1];
        //return new Vector3((float)_x, (float)point.height, (float)_y);
    }

    /// <summary>
    /// 通过经纬高度获取 Unity 3D坐标(含高度)
    /// </summary>
    /// <param name="point"><see cref="Point2"/>对象, 对经纬度的封装</param>
    /// <param name="height">高度</param>
    /// <returns></returns>
    public static Vector3 ToVector(Point2 point, double height)
    {
        double _x = ((point.longitude - 122.136829994473) * -85369.821291030713527972595556599 - 1809.04);
        double _y = ((point.latitude - 37.4688299967702) * -103620.81635379537645599988767665 + 4227.987);
        return new Vector3((float)_x, (float)height, (float)_y);
        //double[] current = LatLonToUTMXY(point2.longitude, point2.latitude);
        //double[] center = LatLonToUTMXY(_longitude, _latitude);
        //double _x = center[0] - current[0];
        //double _y = center[1] - current[1];
        //return new Vector3((float)_x, (float)height, (float)_y);
    }

    /// <summary>
    /// 通过经纬高度获取 Unity 3D坐标(含高度)
    /// </summary>
    /// <param name="longitude">经度</param>
    /// <param name="latitude">纬度</param>
    /// <param name="height">高度</param>
    /// <returns></returns>
    public static Vector3 ToVector(double longitude, double latitude, double height)
    {
//        double _x = ((longitude - 122.136829994473) * -85369.821291030713527972595556599 - 1809.04);
//        double _y = ((latitude - 37.4688299967702) * -103620.81635379537645599988767665 + 4227.987);
//        return new Vector3((float)_x, (float)height, (float)_y);

        double[] current = LatLonToUTMXY(longitude, latitude);
        double[] center = LatLonToUTMXY(_longitude, _latitude);
        double _x = center[0] - current[0];
        double _y = center[1] - current[1];
        return new Vector3((float)_x, (float)height, (float)_y);
    }

    /// <summary>
    /// 通过 Unity 2D坐标(不含高度) 获取经纬度
    /// </summary>
    /// <param name="position"></param>
    /// <returns></returns>
    public static double[] ToLatLon(Vector2 position)
    {
        double[] latLon = new double[2]; 
        latLon[0] = (position.x - 2140) / 85034.617864360044246411962685833 + 122.136829994473;
        latLon[1] = (7609 - position.y - 8312) / -103627.52438550783120400193244459 + 37.4688299967702;
        return latLon;
        
        //double _x = center[0] - position.x;
        //double _y = center[1] - position.y;
        //double _zone = center[2];
        //return UTMXYToLatLon(_x, _y, _zone, false);
    }

    /// <summary>
    /// 通过 Unity 3D坐标(含高度) 获取经纬度
    /// </summary>
    /// <param name="point"><see cref="Point2"/>对象, 对经纬度的封装</param>
    /// <returns></returns>
    public static double[] ToLatLon(Point2 point)
    {
        return point.ToLatLon();
    }

    /// <summary>
    /// 通过 Unity 3D坐标(含高度) 获取经纬度
    /// </summary>
    /// <param name="position"></param>
    /// <returns></returns>
    public static double[] ToLatLon(Vector3 position)
    {
//        double[] latLon = new double[2];
//        latLon[0] = (position.x + 1809.04) / -85369.821291030713527972595556599 + 122.136829994473;
//        latLon[1] = (position.z - 4227.987) / -103620.81635379537645599988767665 + 37.4688299967702;
//        return latLon;
        double[] center = LatLonToUTMXY(_longitude, _latitude);
        double _x = center[0] - position.x;
        double _y = center[1] - position.z;
        double _zone = center[2];
        return UTMXYToLatLon(_x, _y, _zone, false);
    }
    
    /// <summary>
    /// 通过 Unity 3D坐标(含高度) 获取经纬度
    /// </summary>
    /// <param name="point"><see cref="Point3"/>对象, 对经纬高数据的封装</param>
    /// <returns></returns>
    public static double[] ToLatLon(Point3 point)
    {
        return point.ToLatLon();
    }
    
    /// <summary>
    /// <remarks>计算两点位置的距离，返回两点的距离，单位 米</remarks>
    /// 该公式为GOOGLE提供，误差小于0.2米
    /// </summary>
    /// <param name="lat1">第一点纬度</param>
    /// <param name="lng1">第一点经度</param>
    /// <param name="lat2">第二点纬度</param>
    /// <param name="lng2">第二点经度</param>
    /// <returns></returns>
    public static double LatLonDistance(double lat1, double lng1, double lat2, double lng2)
    {
        double radLat1 = DegToRad(lat1);
        double radLng1 = DegToRad(lng1);
        double radLat2 = DegToRad(lat2);
        double radLng2 = DegToRad(lng2);
        double a = radLat1 - radLat2;
        double b = radLng1 - radLng2;
        double result = 2 * Math.Asin(Math.Sqrt(Math.Pow(Math.Sin(a / 2), 2) + Math.Cos(radLat1) * Math.Cos(radLat2) * Math.Pow(Math.Sin(b / 2), 2))) * sm_a;
        return result;
    }
    
    /// <summary>
    /// 三维转二维局部坐标
    /// </summary>
    /// <param name="position"></param>
    /// <returns></returns>
    public static Vector2 WordToMap(Vector3 position)
    {
        Vector3 pos = center - position;
        return new Vector2(pos.x, pos.z);
    }
    
    /// <summary>
    /// 地图局部坐标转世界坐标
    /// </summary>
    /// <param name="position"></param>
    /// <param name="height"></param>
    /// <returns></returns>
    public static Vector3 MapToWord(Vector2 position, float height = 0f)
    {
        Vector3 pos = Vector3.zero;
        pos.x = position.x;
        pos.z = position.y;
        center.y = height;
        return center - pos;
    }
}