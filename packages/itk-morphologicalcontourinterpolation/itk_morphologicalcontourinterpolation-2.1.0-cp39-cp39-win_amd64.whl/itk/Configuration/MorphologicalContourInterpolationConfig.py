depends = ('ITKPyBase', 'ITKDistanceMap', 'ITKBinaryMathematicalMorphology', )
templates = (  ('MorphologicalContourInterpolator', 'itk::MorphologicalContourInterpolator', 'itkMorphologicalContourInterpolatorIUS3', True, 'itk::Image< unsigned short,3 >'),
  ('MorphologicalContourInterpolator', 'itk::MorphologicalContourInterpolator', 'itkMorphologicalContourInterpolatorIUC3', True, 'itk::Image< unsigned char,3 >'),
  ('MorphologicalContourInterpolator', 'itk::MorphologicalContourInterpolator', 'itkMorphologicalContourInterpolatorISS3', True, 'itk::Image< signed short,3 >'),
)
factories = ()
