# cmip7-strat-aerosol



## Getting started

### Install the package
```
pip install cmip7-strat-aerosol
```


### Create a config file


```yaml
output:
  model: CanESM
  folder: 'path/to/output/directory'
  bands:
    shortwave:
      source:
        planck:
          temperature: 5777.0  # Kelvin
      units: cm-1  # cm-1, nm or m
      bounds: [[50000, 14500], [14500, 8400], [8400, 4200], [4200, 2500]]
    longwave:
      source:
        planck:
          temperature: 223.0  # Kelvin
      units: cm-1
      bounds: [[2200, 2500], [1900, 2200], [1400, 1900], [1100, 1400], [980, 1100], [800, 980], [540, 800], [340, 540], [100, 340]]

input:
  folder: /path/to/stratospheric/aerosol/files/v1.3
  base_filename: input4MIPs_aerosolProperties_CMIP_UOEXETER-CMIP-1-3-0_gnz_175001-202312.nc
```

### Run the program

```
convert-cmip7 config.yaml
```